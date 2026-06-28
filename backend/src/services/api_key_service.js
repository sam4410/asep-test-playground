/**
 * API Key Validation Service
 *
 * This module encapsulates the logic for validating API keys.
 * In a real‑world scenario the keys would be stored in a database,
 * cache (e.g., Redis) or a secret manager. For the purpose of this
 * playground we keep a static in‑memory list that can be easily
 * extended in tests.
 *
 * The service exports a single async function `isValidApiKey`
 * which returns a boolean indicating whether the supplied key is
 * recognised as valid.
 */

// Example static store – replace with DB/Cache lookup as needed
const VALID_API_KEYS = new Set([
  // These keys are deliberately simple for testing; in production
  // they should be long, random, and stored securely.
  'test-key-123',
  'demo-key-456',
]);

/**
 * Checks if the provided API key is valid.
 *
 * @param {string} apiKey - The API key supplied by the client.
 * @returns {Promise<boolean>} Resolves to true if the key is valid, otherwise false.
 */
async function isValidApiKey(apiKey) {
  // Guard against undefined/null values early
  if (!apiKey || typeof apiKey !== 'string') {
    return false;
  }

  // In a real implementation this would be an async DB/Cache call.
  // Using Set.has provides O(1) lookup and keeps the function async
  // for compatibility with future async data sources.
  return VALID_API_KEYS.has(apiKey);
}

module.exports = {
  isValidApiKey,
};

// Export for testing convenience (optional)
if (process.env.NODE_ENV === 'test') {
  module.exports._VALID_API_KEYS = VALID_API_KEYS;
}