// Simple Express server with /api/v1/gamma endpoint
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON (not strictly needed for this endpoint)
app.use(express.json());

/**
 * GET /api/v1/gamma
 * Returns the word "gamma" in the response body.
 * The response is a JSON object: { "word": "gamma" }
 */
app.get('/api/v1/gamma', (req, res) => {
  res.json({ word: 'gamma' });
});

// Health check endpoint (optional)
app.get('/health', (req, res) => {
  res.send('OK');
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

module.exports = app;