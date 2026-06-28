/**
 * Unit tests for the API Key Validation Service.
 *
 * The service exposes a single async function `isValidApiKey`.
 * In test mode the internal Set of valid keys is also exported as
 * `_VALID_API_KEYS` to allow manipulation (e.g., adding an "expired"
 * key for testing purposes).
 *
 * These tests cover:
 *   - A known valid key
 *   - An unknown/invalid key
 *   - A malformed key (non‑string)
 *   - Missing key (undefined / null)
 *   - An “expired” key simulated by removing it from the Set
 */

const { isValidApiKey, _VALID_API_KEYS } = require('../src/services/api_key_service');
const assert = require('assert');

describe('API Key Validation Service', () => {
  const VALID_KEY = 'test-key-123';
  const INVALID_KEY = 'invalid-key-999';

  afterEach(() => {
    // Ensure the static Set is restored after each test that mutates it
    _VALID_API_KEYS.clear();
    _VALID_API_KEYS.add('test-key-123');
    _VALID_API_KEYS.add('demo-key-456');
  });

  it('should return true for a known valid API key', async () => {
    const result = await isValidApiKey(VALID_KEY);
    assert.strictEqual(result, true);
  });

  it('should return false for an unknown API key', async () => {
    const result = await isValidApiKey(INVALID_KEY);
    assert.strictEqual(result, false);
  });

  it('should return false for a malformed (non‑string) API key', async () => {
    const result = await isValidApiKey(12345);
    assert.strictEqual(result, false);
  });

  it('should return false when the API key is missing (undefined)', async () => {
    const result = await isValidApiKey(undefined);
    assert.strictEqual(result, false);
  });

  it('should treat a key that has been removed from the store as expired/invalid', async () => {
    // Simulate expiration by deleting the key from the Set
    _VALID_API_KEYS.delete(VALID_KEY);
    const result = await isValidApiKey(VALID_KEY);
    assert.strictEqual(result, false);
  });
});