import { useEffect, useState } from "react";
import {
  fetchSettings,
  getCachedSettings,
  resetSettings,
  updateSettings,
  type SettingsResponse,
  type SettingsUpdate,
} from "../src/lib/settingsClient";

const THEME_OPTIONS = [
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
  { value: "system", label: "System" },
];

const LANGUAGE_OPTIONS = [
  { value: "en", label: "English" },
  { value: "es", label: "Español" },
  { value: "fr", label: "Français" },
];

type LoadState = "loading" | "ready" | "error";

/**
 * Full settings screen: account preferences (theme, language, timezone,
 * notifications) backed by the /settings API, plus a danger zone for
 * resetting preferences to defaults.
 */
export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(
    getCachedSettings()
  );
  const [loadState, setLoadState] = useState<LoadState>(
    settings ? "ready" : "loading"
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [confirmingReset, setConfirmingReset] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetchSettings()
      .then((data) => {
        if (cancelled) return;
        setSettings(data);
        setLoadState("ready");
        setError(null);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err instanceof Error ? err.message : "Something went wrong.");
        setLoadState((prev) => (settings ? "ready" : "error"));
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function applyUpdate(update: SettingsUpdate) {
    if (!settings) return;
    const previous = settings;
    const optimistic = { ...settings, ...update };
    setSettings(optimistic);
    setSaving(true);
    setError(null);
    try {
      const saved = await updateSettings(update);
      setSettings(saved);
    } catch (err) {
      setSettings(previous);
      setError(
        err instanceof Error ? err.message : "Failed to save your changes."
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleReset() {
    setSaving(true);
    setError(null);
    try {
      const fresh = await resetSettings();
      setSettings(fresh);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to reset settings."
      );
    } finally {
      setSaving(false);
      setConfirmingReset(false);
    }
  }

  if (loadState === "loading") {
    return (
      <div className="flex items-center justify-center py-24">
        <p className="text-sm text-subtext">Loading settings…</p>
      </div>
    );
  }

  if (loadState === "error" || !settings) {
    return (
      <div className="rounded-2xl border border-dashed border-border bg-card p-6 text-center">
        <p className="text-sm text-danger">
          {error ?? "Couldn't load settings. Please try again."}
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold text-text">Settings</h1>
        <p className="text-sm text-subtext">
          Manage your appearance, notification, and account preferences.
        </p>
      </header>

      {error && (
        <p className="rounded-xl border border-danger/30 bg-danger/5 p-3 text-sm text-danger">
          {error}
        </p>
      )}

      <section className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-5 shadow-sm">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-subtext">
          Appearance
        </h2>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <label htmlFor="theme" className="text-sm font-medium text-text">
            Theme
          </label>
          <select
            id="theme"
            value={settings.theme}
            disabled={saving}
            onChange={(e) => applyUpdate({ theme: e.target.value })}
            className="rounded-xl border border-border bg-background px-3 py-1.5 text-sm text-text outline-none focus:border-primary"
          >
            {THEME_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <label htmlFor="language" className="text-sm font-medium text-text">
            Language
          </label>
          <select
            id="language"
            value={settings.language}
            disabled={saving}
            onChange={(e) => applyUpdate({ language: e.target.value })}
            className="rounded-xl border border-border bg-background px-3 py-1.5 text-sm text-text outline-none focus:border-primary"
          >
            {LANGUAGE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <label htmlFor="timezone" className="text-sm font-medium text-text">
            Timezone
          </label>
          <input
            id="timezone"
            type="text"
            value={settings.timezone}
            disabled={saving}
            placeholder="e.g. America/New_York"
            onBlur={(e) => applyUpdate({ timezone: e.target.value.trim() })}
            onChange={(e) =>
              setSettings({ ...settings, timezone: e.target.value })
            }
            className="w-56 rounded-xl border border-border bg-background px-3 py-1.5 text-sm text-text outline-none focus:border-primary"
          />
        </div>
      </section>

      <section className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-5 shadow-sm">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-subtext">
          Notifications
        </h2>

        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-text">Email notifications</p>
            <p className="text-xs text-subtext">
              Receive habit summaries and reminders by email.
            </p>
          </div>
          <button
            type="button"
            role="switch"
            aria-checked={settings.email_notifications}
            disabled={saving}
            onClick={() =>
              applyUpdate({ email_notifications: !settings.email_notifications })
            }
            aria-label="Email notifications"
            className={`h-6 w-11 rounded-full transition-colors ${
              settings.email_notifications ? "bg-primary" : "bg-border"
            }`}
          >
            <span
              className={`block h-5 w-5 translate-x-0.5 rounded-full bg-white shadow transition-transform ${
                settings.email_notifications ? "translate-x-5