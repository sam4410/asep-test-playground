export type SettingsResponse = {
  theme: string;
  language: string;
  timezone: string;
  email_notifications: boolean;
  push_notifications: boolean;
};

export type SettingsUpdate = Partial<SettingsResponse>;

const DEFAULT_SETTINGS: SettingsResponse = {
  theme: "system",
  language: "en",
  timezone: "UTC",
  email_notifications: true,
  push_notifications: true,
};

const STORAGE_KEY = "app.settings.cache";

function getApiBase(): string {
  if (typeof process !== "undefined" && process.env && process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }
  return "/api";
}

export function getCachedSettings(): SettingsResponse | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as SettingsResponse;
  } catch {
    return null;
  }
}

function setCachedSettings(settings: SettingsResponse): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // ignore storage errors
  }
}

export async function fetchSettings(): Promise<SettingsResponse> {
  try {
    const res = await fetch(`${getApiBase()}/settings`, {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) {
      throw new Error(`Failed to load settings (status ${res.status})`);
    }
    const data = (await res.json()) as SettingsResponse;
    setCachedSettings(data);
    return data;
  } catch (err) {
    const cached = getCachedSettings();
    if (cached) return cached;
    setCachedSettings(DEFAULT_SETTINGS);
    return DEFAULT_SETTINGS;
  }
}

export async function updateSettings(
  update: SettingsUpdate
): Promise<SettingsResponse> {
  const res = await fetch(`${getApiBase()}/settings`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(update),
  });
  if (!res.ok) {
    throw new Error(`Failed to save settings (status ${res.status})`);
  }
  const data = (await res.json()) as SettingsResponse;
  setCachedSettings(data);
  return data;
}

export async function resetSettings(): Promise<SettingsResponse> {
  const res = await fetch(`${getApiBase()}/settings/reset`, {
    method: "POST",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`Failed to reset settings (status ${res.status})`);
  }
  const data = (await res.json()) as SettingsResponse;
  setCachedSettings(data);
  return data;
}
