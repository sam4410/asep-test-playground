const express = require('express');
const router = express.Router();

// Service that knows how to retrieve coupon discounts
const { getDiscount } = require('../../../services/coupon_service');

/**
 * GET /api/v1/coupons/:code
 *
 * Returns the discount percentage for a valid coupon code.
 *
 * Responses:
 *   200 { discount: number }          – when the coupon exists and is valid
 *   400 { error: "Invalid coupon code format" } – when the code does not match expected pattern
 *   404 { error: "Coupon not found" } – when the code is well‑formed but not recognised
 *   500 { error: "Internal server error" } – on unexpected errors
 */
router.get('/:code', async (req, res) => {
  const { code } = req.params;

  // Basic format validation – delegate to service for consistency
  try {
    const discount = await getDiscount(code);
    if (discount === null) {
      // Well‑formed but unknown coupon
      return res.status(404).json({ error: 'Coupon not found' });
    }
    // Success
    return res.status(200).json({ discount });
  } catch (err) {
    if (err.message === 'Invalid format') {
      return res.status(400).json({ error: 'Invalid coupon code format' });
    }
    console.error('Coupon validation error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;
