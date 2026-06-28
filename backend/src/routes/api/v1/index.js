const express = require('express');
const router = express.Router();

// Import sub‑routes
const planetsRouter = require('./planets');
const citiesRouter = require('./cities');

// Mount sub‑routes
router.use('/planets', planetsRouter);
router.use('/cities', citiesRouter);

// Default route for API version root
router.get('/', (req, res) => {
  res.json({ message: 'API v1 root' });
});

module.exports = router;
