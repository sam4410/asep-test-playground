/**
 * Service responsible for validating API keys.
 *
 * In a real implementation this would query a database or another
 * persistent store. For the purposes of this exercise we keep a simple
 * in‑memory list of keys. The function is asynchronous to mirror the
 * typical I/O pattern of a real data source.
 */

// Example set of valid API keys. In production this would be replaced
// with a secure lookup (e.g., a DB query or external secrets manager).
const VALID_API_KEYS = new Set([
  // These are placeholder keys used only for testing.
  'test-key-123',
  'demo-key-456',
  'prod-key-789',
]);

/**
 * Checks whether the supplied API key is recognised.
 *
 * @param {string} apiKey - The API key to validate.
 * @returns {Promise<boolean>} Resolves to true if the key is valid,
 *                             otherwise false.
 */
async function isValidApiKey(apiKey) {
  // Guard against non‑string input – treat as invalid.
  if (typeof apiKey !== 'string') {
    return false;
  }

  // Simulate async behaviour (e.g., DB call) using a resolved promise.
  return Promise.resolve(VALID_API_KEYS.has(apiKey));
}

module.exports = {
  isValidApiKey,
};
