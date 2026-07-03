const { expect } = require('chai');
const sinon = require('sinon');

// The service uses in‑memory Maps, so each test should start with a fresh copy.
// We'll require the module anew for each test case.
function loadService() {
  // Delete from require cache to reset the Maps
  delete require.cache[require.resolve('../src/services/auth_service')];
  return require('../src/services/auth_service');
}

describe('Auth Service', () => {
  let authService;\n+
  beforeEach(() => {
    authService = loadService();
  });

  describe('registerUser', () => {
    it('should register a new user and return verification token', async () => {
      const result = await authService.registerUser({
        email: 'test@example.com',
        password: 'Secret123',
        name: 'Tester',
      });
      expect(result).to.have.property('id');
      expect(result).to.have.property('verificationToken');
      expect(result.email).to.equal('test@example.com');
    });

    it('should throw when registering an existing email', async () => {
      await authService.registerUser({
        email: 'dup@example.com',
        password: 'pwd',
        name: 'Dup',
      });
      try {
        await authService.registerUser({
          email: 'dup@example.com',
          password: 'pwd2',
          name: 'Dup2',
        });
        throw new Error('Expected error not thrown');
      } catch (err) {
        expect(err.message).to.equal('User already exists');
      }
    });
  });

  describe('verifyEmail', () => {
    it('should verify email with valid token', async () => {
      const { verificationToken } = await authService.registerUser({
        email: 'verify@example.com',
        password: 'pwd',
        name: 'V',
      });
      await authService.verifyEmail(verificationToken);
      // after verification, login should succeed (tested later)
    });

    it('should throw for invalid token', async () => {
      try {
        await authService.verifyEmail('nonexistent-token');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('Invalid or expired token');
      }
    });
  });

  describe('loginUser', () => {
    it('should login verified user and return tokens', async () => {
      const { verificationToken } = await authService.registerUser({
        email: 'login@example.com',
        password: 'pwd123',
        name: 'L',
      });
      await authService.verifyEmail(verificationToken);
      const tokens = await authService.loginUser('login@example.com', 'pwd123');
      expect(tokens).to.have.property('accessToken');
      expect(tokens).to.have.property('refreshToken');
    });

    it('should reject login for unverified email', async () => {
      await authService.registerUser({
        email: 'unverified@example.com',
        password: 'pwd',
        name: 'U',
      });
      try {
        await authService.loginUser('unverified@example.com', 'pwd');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('Email not verified');
      }
    });

    it('should reject login with wrong password', async () => {
      const { verificationToken } = await authService.registerUser({
        email: 'wrongpwd@example.com',
        password: 'correct',
        name: 'W',
      });
      await authService.verifyEmail(verificationToken);
      try {
        await authService.loginUser('wrongpwd@example.com', 'incorrect');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('Invalid credentials');
      }
    });
  });

  describe('refreshToken', () => {
    it('should issue new access token for valid refresh token', async () => {
      const { verificationToken } = await authService.registerUser({
        email: 'refresh@example.com',
        password: 'pwd',
        name: 'R',
      });
      await authService.verifyEmail(verificationToken);
      const { refreshToken } = await authService.loginUser('refresh@example.com', 'pwd');
      const newAccess = await authService.refreshToken(refreshToken);
      expect(newAccess).to.be.a('string');
    });

    it('should reject invalid refresh token', async () => {
      try {
        await authService.refreshToken('invalid-token');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('Invalid refresh token');
      }
    });
  });

  describe('forgotPassword & resetPassword', () => {
    it('should generate a reset token and allow password reset', async () => {
      const { verificationToken } = await authService.registerUser({
        email: 'reset@example.com',
        password: 'oldpwd',
        name: 'Reset',
      });
      await authService.verifyEmail(verificationToken);
      const token = await authService.forgotPassword('reset@example.com');
      expect(token).to.be.a('string');
      await authService.resetPassword(token, 'newpwd');
      // login with new password should succeed
      const tokens = await authService.loginUser('reset@example.com', 'newpwd');
      expect(tokens).to.have.property('accessToken');
    });

    it('should reject reset with invalid token', async () => {
      try {
        await authService.resetPassword('bad-token', 'pwd');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('Invalid or expired token');
      }
    });
  });

  describe('profile management', () => {
    let userId;\n+
    beforeEach(async () => {
      const { verificationToken, id } = await authService.registerUser({
        email: 'profile@example.com',
        password: 'pwd',
        name: 'Orig',
      });
      await authService.verifyEmail(verificationToken);
      userId = id;
    });

    it('should retrieve user profile without password', async () => {
      const profile = await authService.getProfile(userId);
      expect(profile).to.have.property('email', 'profile@example.com');
      expect(profile).to.have.property('name', 'Orig');
      expect(profile).to.not.have.property('password');
    });

    it('should update profile fields', async () => {
      const updated = await authService.updateProfile(userId, { name: 'Updated' });
      expect(updated.name).to.equal('Updated');
      const fetched = await authService.getProfile(userId);
      expect(fetched.name).to.equal('Updated');
    });

    it('should error when profile not found', async () => {
      try {
        await authService.getProfile('nonexistent-id');
        throw new Error('Expected error');
      } catch (err) {
        expect(err.message).to.equal('User not found');
      }
    });
  });
});