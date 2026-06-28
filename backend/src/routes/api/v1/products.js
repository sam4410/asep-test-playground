const express = require('express');
const router = express.Router();

// Static list of products
const products = [
  { id: 1, name: 'Laptop', price: 999.99 },
  { id: 2, name: 'Smartphone', price: 599.99 },
  { id: 3, name: 'Headphones', price: 199.99 },
  { id: 4, name: 'Keyboard', price: 49.99 },
  { id: 5, name: 'Mouse', price: 29.99 },
];

// GET /api/v1/products
router.get('/', (req, res) => {
  res.json({ products });
});

module.exports = router;

