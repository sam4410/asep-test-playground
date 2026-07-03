const request = require('supertest');
const { expect } = require('chai');

// Helper to load a fresh instance of the Express app for each test suite
function loadApp() {
  delete require.cache[require.resolve('../src/app')];
  return require('../src/app');
}

describe('Auth Integration Flow', () => {
  let app;
  const user = {
    email: 'inttest@example.com',
    password: 'Secret123!',
    name: 'Int Test',
  };
  let verificationToken;
  let accessToken;
  let refreshToken;

  before(() => {
    app = loadApp();
  });

  it('should register a new user and receive verification token', async () => {
    const res = await request(app).post('/api/v1/auth/register').send(user);
    expect(res.status).to.equal(201);
    expect(res.body).to.have.property('verificationToken');
    verificationToken = res.body.verificationToken;
  });

  it('should verify the user email', async () => {
    const res = await request(app)
      .get('/api/v1/auth/verify-email')
      .query({ token: verificationToken });
    expect(res.status).to.equal(200);
    expect(res.body).to.deep.equal({ message: 'Email verified' });
  });

  it('should login and receive access & refresh tokens', async () => {
    const res = await request(app)
      .post('/api/v1/auth/login')
      .send({ email: user.email, password: user.password });
    expect(res.status).to.equal(200);
    expect(res.body).to.have.keys(['accessToken', 'refreshToken']);
    accessToken = res.body.accessToken;
    refreshToken = res.body.refreshToken;
  });

  it('should access protected profile endpoint', async () => {
    const res = await request(app)
      .get('/api/v1/auth/profile')
      .set('Authorization', `Bearer ${accessToken}`);
    expect(res.status).to.equal(200);
    expect(res.body).to.have.property('email', user.email);
    expect(res.body).to.have.property('name', user.name);
  });

  it('should update profile name', async () => {
    const newName = 'Updated Name';
    const res = await request(app)
      .put('/api/v1/auth/profile')
      .set('Authorization', `Bearer ${accessToken}`)
      .send({ name: newName });
    expect(res.status).to.equal(200);
    expect(res.body).to.have.property('name', newName);
  });

  it('should refresh access token', async () => {
    const res = await request(app)
      .post('/api/v1/auth/refresh')
      .send({ refreshToken });
    expect(res.status).to.equal(200);
    expect(res.body).to.have.property('accessToken');
    // replace old access token for further checks
    accessToken = res.body.accessToken;
  });

  it('should initiate forgot‑password flow and receive reset token', async () => {
    const res = await request(app)
      .post('/api/v1/auth/forgot-password')
      .send({ email: user.email });
    expect(res.status).to.equal(200);
    // The service returns the token for demo purposes
    expect(res.body).to.have.property('token');
    verificationToken = res.body.token; // reuse variable for reset token
  });

  it('should reset password using the token', async () => {
    const newPwd = 'NewSecret123!';
    const res = await request(app)
      .post('/api/v1/auth/reset-password')
      .send({ token: verificationToken, newPassword: newPwd });
    expect(res.status).to.equal(200);
    expect(res.body).to.deep.equal({ message: 'Password reset' });

    // login with new password should succeed
    const loginRes = await request(app)
      .post('/api/v1/auth/login')
      .send({ email: user.email, password: newPwd });
    expect(loginRes.status).to.equal(200);
    expect(loginRes.body).to.have.property('accessToken');
  });
});