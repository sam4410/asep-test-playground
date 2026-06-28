/**
 * Tests for the API key validation endpoint.
 *
 * Covers:
 *   - Valid API key returns 200 { valid: true }
 *   - Invalid API key returns 401 { valid: false }
 *   - Missing apiKey field returns 400 with error message
 *   - Non‑string apiKey (e.g., number) is treated as invalid → 401
 */

const request = require('supertest');
const app = require('../src/app');

describe('POST /api/v1/validate-key', () => {
  const endpoint = '/api/v1/validate-key';

  test('returns 200 and valid:true for a known good key', async () => {
    const res = await request(app)
      .post(endpoint)
      .send({ apiKey: 'test-key-123' })
      .set('Accept', 'application/json');

    expect(res.status).toBe(200);
    expect(res.body).toEqual({ valid: true });
  });

  test('returns 401 and valid:false for an unknown key', async () => {
    const res = await request(app)
      .post(endpoint)
      .send({ apiKey: 'unknown-key-000' })
      .set('Accept', 'application/json');

    expect(res.status).toBe(401);
    expect(res.body).toEqual({ valid: false });
  });

  test('returns 400 when apiKey is missing from payload', async () => {
    const res = await request(app)
      .post(endpoint)
      .send({})\n+      .set('Accept', 'application/json');\n+\n+    expect(res.status).toBe(400);\n+    expect(res.body).toHaveProperty('error');\n+    expect(res.body.error).toMatch(/Missing apiKey/);\n+  });\n+\n+  test('returns 401 when apiKey is not a string (e.g., number)', async () => {\n+    const res = await request(app)\n+      .post(endpoint)\n+      .send({ apiKey: 12345 })\n+      .set('Accept', 'application/json');\n+\n+    expect(res.status).toBe(401);\n+    expect(res.body).toEqual({ valid: false });\n+  });\n+});\n+\n+/**\n+ * Unit tests for the service layer directly.\n+ */\n+const { isValidApiKey } = require('../src/services/api_key_service');\n+\n+describe('api_key_service.isValidApiKey', () => {\n+  test('recognises a valid key', async () => {\n+    await expect(isValidApiKey('demo-key-456')).resolves.toBe(true);\n+  });\n+\n+  test('rejects an invalid key', async () => {\n+    await expect(isValidApiKey('bad-key')).resolves.toBe(false);\n+  });\n+\n+  test('rejects non‑string input', async () => {\n+    await expect(isValidApiKey(null)).resolves.toBe(false);\n+    await expect(isValidApiKey(undefined)).resolves.toBe(false);\n+    await expect(isValidApiKey(123)).resolves.toBe(false);\n+  });\n+});\n+\n*** End of File ***