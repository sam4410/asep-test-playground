const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const validateKeyRouter = require('./routes/api/v1/validate_key');

// Middleware
app.use(bodyParser.json());

