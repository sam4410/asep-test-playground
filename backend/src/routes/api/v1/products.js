const express = require('express');
const router = express.Router();

// Sample static list of products
// In a real implementation this would query a database.
const products = [
  { id: 1, name: 'Apple iPhone', category: 'electronics', price: 999 },
  { id: 2, name: 'Banana', category: 'grocery', price: 1 },
  { id: 3, name: 'Samsung TV', category: 'electronics', price: 499 },
  { id: 4, name: 'Bread', category: 'grocery', price: 2 },
  { id: 5, name: 'Leather Wallet', category: 'accessories', price: 45 },
  { id: 6, name: 'Running Shoes', category: 'footwear', price: 120 },
  { id: 7, name: 'Coffee Mug', category: 'kitchen', price: 15 },
  { id: 8, name: 'Desk Lamp', category: 'furniture', price: 30 },
  { id: 9, name: 'Headphones', category: 'electronics', price: 199 },
  { id: 10, name: 'Orange Juice', category: 'grocery', price: 3 },
];

/**
 * Helper to apply sorting based on a comma‑separated list.
 * Example: sort=price:desc,name:asc
 */
function applySorting(data, sortParam) {
  if (!sortParam) return data;
  const sortFields = sortParam.split(',').map((s) => {
    const [field, dir] = s.split(':');
    return { field, dir: dir === 'desc' ? -1 : 1 };
  });
  return data.slice().sort((a, b) => {
    for (const { field, dir } of sortFields) {
      if (a[field] < b[field]) return -1 * dir;
      if (a[field] > b[field]) return 1 * dir;
    }
    return 0;
  });
}

// GET /api/v1/products
router.get('/', (req, res) => {
  const {
    page = '1',
    limit = '10',
    category,
    min_price,
    max_price,
    sort,
  } = req.query;

  let filtered = products;

  // Category filter
  if (category) {
    filtered = filtered.filter((p) => p.category === category);
  }

  // Price range filter
  const minPriceNum = parseFloat(min_price);
  const maxPriceNum = parseFloat(max_price);
  if (!Number.isNaN(minPriceNum)) {
    filtered = filtered.filter((p) => p.price >= minPriceNum);
  }
  if (!Number.isNaN(maxPriceNum)) {
    filtered = filtered.filter((p) => p.price <= maxPriceNum);
  }

  // Sorting
  filtered = applySorting(filtered, sort);

  // Pagination
  const pageNum = Math.max(parseInt(page, 10), 1);
  const limitNum = Math.max(parseInt(limit, 10), 1);
  const startIdx = (pageNum - 1) * limitNum;
  const paged = filtered.slice(startIdx, startIdx + limitNum);

  res.json({
    products: paged,
    meta: {
      total: filtered.length,
      page: pageNum,
      limit: limitNum,
    },
  });
});

module.exports = router;
