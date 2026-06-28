/**
 * Integration tests for the /api/v1/validate-key endpoint.
 *
 * These tests spin up a minimal Express instance, mount the
 * validate‑key router and issue HTTP requests using supertest.
 * They verify that the endpoint returns the correct status codes
 * and payloads for various API‑key scenarios.
 */

const express = require('express');
const request = require('supertest');
const bodyParser = require('express').json;

// Router under test
const validateKeyRouter = require('../src/routes/api/v1/validate_key');

// Helper to create an app with the router mounted
function createApp() {
  const app = express();
  app.use(bodyParser());
  // Mount at the same path as in production
  app.use('/api/v1/validate-key', validateKeyRouter);
  return app;
}

describe('POST /api/v1/validate-key', () => {
  const app = createApp();

  it('should return 200 and { valid: true } for a known valid key', async () => {
    const res = await request(app)
      .post('/api/v1/validate-key')
      .send({ apiKey: 'test-key-123' })
      .set('Accept', 'application/json');

    expect(res.status).toBe(200);
    expect(res.body).toEqual({ valid: true });
  });

  it('should return 401 and { valid: false } for an unknown/invalid key', async () => {
    const res = await request(app)
      .post('/api/v1/validate-key')
      .send({ apiKey: 'invalid-key-999' })
      .set('Accept', 'application/json');

    expect(res.status).toBe(401);
    expect(res.body).toEqual({ valid: false });
  });

  it('should return 400 when apiKey is missing from the request body', async () => {
    const res = await request(app)
      .post('/api/v1/validate-key')
      .send({ }) // no apiKey
      .set('Accept', 'application/json');

    expect(res.status).toBe(400);
    expect(res.body).toHaveProperty('error');
  });

  it('should return 400 when request body is not JSON', async () => {
    const res = await request(app)
      .post('/api/v1/validate-key')
      .set('Content-Type', 'text/plain')
      .send('apiKey=whatever');

    // Express json parser will reject the payload and respond with 400
    expect(res.status).toBe(400);
  });
});