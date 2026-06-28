/**
 * Simple API key validation service.
 *
 * In a real‑world scenario this would query a database or an external
 * authentication provider. For the purposes of this repository we keep the
 * implementation lightweight and configurable via an environment variable.
 *
 * The environment variable `VALID_API_KEYS` should contain a comma‑separated
 * list of keys that are considered valid, e.g.:
 *
 *   VALID_API_KEYS=key1,key2,key3
 *
 * If the variable is not set, the service will treat **no** keys as valid.
 */

// Load the list of valid keys once at module load time.
const VALID_API_KEYS = process.env.VALID_API_KEYS
  ? process.env.VALID_API_KEYS.split(',').map((k) => k.trim()).filter(Boolean)
  : [];

/**
 * Checks whether the supplied API key is recognised.
 *
 * @param {string} apiKey - The API key supplied by the client.
 * @returns {Promise<boolean>} Resolves to true if the key is valid, otherwise false.
 */
async function isValidApiKey(apiKey) {
  // Guard against non‑string input – treat as invalid.
  if (typeof apiKey !== 'string') {
    return false;
  }

  // Simple in‑memory lookup; case‑sensitive match.
  return VALID_API_KEYS.includes(apiKey);
}

module.exports = {
  isValidApiKey,
};
