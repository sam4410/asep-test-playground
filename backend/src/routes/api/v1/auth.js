const express = require('express');
const router = express.Router();
const {
  registerUser,
  verifyEmail,
  loginUser,
  refreshToken,
  getProfile,
  updateProfile,
  forgotPassword,
  resetPassword,
} = require('../../services/auth_service');
const { authenticate } = require('../../middleware/auth');

// Register new user
router.post('/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    if (!email || !password) {
      return res.status(400).json({ error: 'email and password required' });
    }
    const result = await registerUser({ email, password, name });
    return res.status(201).json(result);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Email verification
router.get('/verify-email', async (req, res) => {
  try {
    const { token } = req.query;
    if (!token) return res.status(400).json({ error: 'Missing token' });
    await verifyEmail(token);
    return res.status(200).json({ message: 'Email verified' });
  } catch (err) {
    console.error(err);
    return res.status(400).json({ error: err.message });
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ error: 'email and password required' });
    }
    const tokens = await loginUser(email, password);
    return res.status(200).json(tokens);
  } catch (err) {
    console.error(err);
    return res.status(401).json({ error: err.message });
  }
});

// Refresh token
router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken: token } = req.body;
    if (!token) return res.status(400).json({ error: 'Missing refresh token' });
    const newAccess = await refreshToken(token);
    return res.status(200).json({ accessToken: newAccess });
  } catch (err) {
    console.error(err);
    return res.status(401).json({ error: err.message });
  }
});

// Forgot password
router.post('/forgot-password', async (req, res) => {
  try {
    const { email } = req.body;
    if (!email) return res.status(400).json({ error: 'Missing email' });
    await forgotPassword(email);
    return res.status(200).json({ message: 'Reset link sent' });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Reset password
router.post('/reset-password', async (req, res) => {
  try {
    const { token, newPassword } = req.body;
    if (!token || !newPassword) return res.status(400).json({ error: 'Missing fields' });
    await resetPassword(token, newPassword);
    return res.status(200).json({ message: 'Password reset' });
  } catch (err) {
    console.error(err);
    return res.status(400).json({ error: err.message });
  }
});

// Profile CRUD (protected)
router.get('/profile', authenticate, async (req, res) => {
  try {
    const profile = await getProfile(req.user.id);
    return res.status(200).json(profile);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

router.put('/profile', authenticate, async (req, res) => {
  try {
    const updated = await updateProfile(req.user.id, req.body);
    return res.status(200).json(updated);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
