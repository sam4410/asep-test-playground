const request = require('supertest');
const { expect } = require('chai');
const proxyquire = require('proxyquire');
const express = require('express');

/**
 * Helper to create an Express app instance with the coupons router mounted.
 * Allows us to inject a stubbed service when needed.
 *
 * @param {object} [stubs] - Optional map of module paths to stub implementations.
 * @returns {Express.Application}
 */
function createApp(stubs = {}) {
  // Load the router, possibly with stubbed service
  const router = proxyquire('../src/routes/api/v1/coupons', stubs);
  const app = express();
  app.use(express.json());
  app.use('/api/v1/coupons', router);
  // Error handling middleware to catch async errors (Express 4)
  app.use((err, req, res, next) => {
    res.status(500).json({ error: 'Internal server error' });
  });
  return app;
}

describe('GET /api/v1/coupons/:code', () => {
  it('returns 200 and discount for a known, well‑formed coupon', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/coupons/SAVE10');
    expect(res.status).to.equal(200);
    expect(res.body).to.have.property('discount', 10);
  });

  it('is case‑insensitive for known coupons', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/coupons/save10');
    expect(res.status).to.equal(200);
    expect(res.body).to.have.property('discount', 10);
  });

  it('returns 404 for a well‑formed but unknown coupon', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/coupons/UNKNOWN');
    expect(res.status).to.equal(404);
    expect(res.body).to.have.property('error', 'Coupon not found');
  });

  it('returns 400 for a malformed coupon code', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/coupons/invalid!'); // contains non‑alphanumeric and wrong length
    expect(res.status).to.equal(400);
    expect(res.body).to.have.property('error', 'Invalid coupon code format');
  });

  it('returns 400 when code is not a string (e.g., numeric path param)', async () => {
    const app = createApp();
    const res = await request(app).get('/api/v1/coupons/123456'); // numeric but still string, passes regex; use stub to simulate non‑string
    // To truly test non‑string handling we stub the service to receive a non‑string.
    const stubService = {
      getDiscount: sinon.stub().callsFake((code) => {
        // Simulate the service receiving a non‑string (should not happen via Express)
        if (typeof code !== 'string') throw new Error('Invalid format');
        return null;
      }),
    };
    const appWithStub = createApp({ '../../../services/coupon_service': stubService });
    const resStub = await request(appWithStub).get('/api/v1/coupons/123456');
    expect(resStub.status).to.equal(400);
    expect(resStub.body).to.have.property('error', 'Invalid coupon code format');
  });

  it('returns 500 when the service throws an unexpected error', async () => {
    const stubService = {
      getDiscount: sinon.stub().rejects(new Error('boom')),
    };
    const app = createApp({ '../../../services/coupon_service': stubService });
    const res = await request(app).get('/api/v1/coupons/SAVE10');
    expect(res.status).to.equal(500);
    expect(res.body).to.have.property('error', 'Internal server error');
  });
});

