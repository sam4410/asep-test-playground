/**
 * Unit tests for frontend/src/lib/settingsClient.ts
 *
 * Covers: fetchSettings, updateSettings, resetSettings, getCachedSettings,
 * and the internal caching/auth-header behavior exercised through the
 * public API. fetch and localStorage are mocked so tests run in isolation.
 */

import {
  fetchSettings,
  updateSettings,
  resetSettings,
  getCachedSettings,
  type SettingsResponse,
} from "../settingsClient";

const CACHE_KEY = "habit-tracker:settings-cache";

const sampleSettings: SettingsResponse = {
  id: "settings-1",
  user_id: "user-1",
  theme: "light",
  language: "en",
  email_notifications: true,
  push_notifications: false,
  timezone: "UTC",
  created_at: "2024-01-01T00:00:00Z",
  updated_at: "2024-01-01T00:00:00Z",
};

function mockFetchOnce(body: unknown, ok = true, status = 200) {
  return jest.fn().mockResolvedValueOnce({
    ok,
    status,
    json: async () => body,
  });
}

describe("settingsClient", () => {
  beforeEach(() => {
    window.localStorage.clear();
    jest.restoreAllMocks();
  });

  describe("getCachedSettings", () => {
    it("returns null when no cache entry exists", () => {
      expect(getCachedSettings()).toBeNull();
    });

    it("returns the parsed settings when a valid cache entry exists", () => {
      window.localStorage.setItem(CACHE_KEY, JSON.stringify(sampleSettings));
      expect(getCachedSettings()).toEqual(sampleSettings);
    });

    it("returns null when the cache entry is malformed JSON (edge case)", () => {
      window.localStorage.setItem(CACHE_KEY, "{not-valid-json");
      expect(getCachedSettings()).toBeNull();
    });
  });

  describe("fetchSettings", () => {
    it("fetches settings from the API and caches the result (happy path)", async () => {
      global.fetch = mockFetchOnce(sampleSettings) as unknown as typeof fetch;

      const result = await fetchSettings();

      expect(result).toEqual(sampleSettings);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/settings"),
        expect.objectContaining({ method: "GET" })
      );
      expect(getCachedSettings()).toEqual(sampleSettings);
    });

    it("includes an Authorization header when a token is present in localStorage", async () => {
      window.localStorage.setItem("access_token", "test-token-123");
      global.fetch = mockFetchOnce(sampleSettings) as unknown as typeof fetch;

      await fetchSettings();

      const callArgs = (global.fetch as jest.Mock).mock.calls[0];
      const options = callArgs[1] as RequestInit;
      expect((options.headers as Record<string, string>).Authorization).toBe(
        "Bearer test-token-123"
      );
    });

    it("throws an error when the response is not ok (edge case)", async () => {
      global.fetch = mockFetchOnce({}, false, 401) as unknown as typeof fetch;

      await expect(fetchSettings()).rejects.toThrow(
        "Failed to load settings (401)"
      );
      // Cache should remain untouched on failure
      expect(getCachedSettings()).toBeNull();
    });
  });

  describe("updateSettings", () => {
    it("sends a PATCH request with the update payload and caches the response (happy path)", async () => {
      const updated = { ...sampleSettings, theme: "dark" };
      global.fetch = mockFetchOnce(updated) as unknown as typeof fetch;

      const result = await updateSettings({ theme: "dark" });

      expect(result).toEqual(updated);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/settings"),
        expect.objectContaining({
          method: "PATCH",
          body: JSON.stringify({ theme: "dark" }),
        })
      );
      expect(getCachedSettings()).toEqual(updated);
    });

    it("sets Content-Type header to application/json", async () => {
      global.fetch = mockFetchOnce(sampleSettings) as unknown as typeof fetch;

      await updateSettings({ language: "es" });

      const callArgs = (global.fetch as jest.Mock).mock.calls[0];
      const options = callArgs[1] as RequestInit;
      expect(
        (options.headers as Record<string, string>)["Content-Type"]
      ).toBe("application/json");
    });

    it("throws an error when the update request fails (edge case)", async () => {
      global.fetch = mockFetchOnce({}, false, 500) as unknown as typeof fetch;

      await expect(updateSettings({ theme: "dark" })).rejects.toThrow(
        "Failed to update settings (500)"
      );
    });

    it("handles an empty update payload without throwing (edge case)", async () => {
      global.fetch = mockFetchOnce(sampleSettings) as unknown as typeof fetch;

      const result = await updateSettings({});

      expect(result).toEqual(sampleSettings);
      const callArgs = (global.fetch as jest.Mock).mock.calls[0];
      const options = callArgs[1] as RequestInit;
      expect(options.body).toBe("{}");
    });
  });

  describe("resetSettings", () => {
    it("sends a POST request to /settings/reset and caches the response (happy path)", async () => {
      global.fetch = mockFetchOnce(sampleSettings) as unknown as typeof fetch;

      const result = await resetSettings();

      expect(result).toEqual(sampleSettings);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/settings/reset"),
        expect.objectContaining({ method: "POST" })
      );
      expect(getCachedSettings()).toEqual(sampleSettings);
    });

    it("throws an error when the reset request fails (edge case)", async () => {
      global.fetch = mockFetchOnce({}, false, 503) as unknown as typeof fetch;

      await expect(resetSettings()).rejects.toThrow(
        "Failed to reset settings (503)"
      );
    });
  });
});
