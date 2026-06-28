const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const validateKeyRouter = require('./routes/api/v1/validate_key');

// Middleware
app.use(bodyParser.json());

// Routes
app.use('/api/v1/validate-key', validateKeyRouter);

// Export for testing
module.exports = app;
