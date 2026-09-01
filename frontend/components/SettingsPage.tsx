import { useEffect, useState } from "react";
import { habitStore } from "../lib/habitStore"; // Corrected import path
import {
  fetchSettings,
  getCachedSettings,
  resetSettings,
  updateSettings,
  type SettingsResponse,
  type SettingsUpdate,
} from "../lib/settingsClient"; // Corrected import path
import ReminderSettings from "./ReminderSettings";
import TimePicker from "./TimePicker"; // Importing the new TimePicker component

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
 * resetting preferences and a link out to the existing per-habit
 * ReminderSettings component so reminder scheduling stays configurable
 * from the same place.
 */
export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(
    getCachedSettings()
  );
  const [loadState, setLoadState] = useState<LoadState>(
    settings ? "ready" : "loading"
  );
  const [resetTime, setResetTime] = useState<string>("08:00"); // Default reset time
  const [notificationsEnabled, setNotificationsEnabled] = useState<boolean>(false); // State for notifications
  const [theme, setTheme] = useState<string>("light"); // Default theme

  useEffect(() => {
    if (loadState === "loading") {
      fetchSettings().then((fetchedSettings) => {
        setSettings(fetchedSettings);
        setLoadState("ready");
        setTheme(fetchedSettings.theme || "light"); // Set theme from fetched settings or default to light
      }).catch(() => {
        setLoadState("error");
      });
    }
  }, [loadState]);

  const handleResetTimeChange = (time: string) => {
    setResetTime(time);
  };

  const handleToggleNotifications = (enabled: boolean) => {
    setNotificationsEnabled(enabled);
    // Logic to handle enabling/disabling notifications can be added here
  };

  const handleThemeChange = (selectedTheme: string) => {
    setTheme(selectedTheme);
    // Logic to handle theme change can be added here
  };

  const handleUpdateSettings = async () => {
    if (settings) {
      await updateSettings({ notificationsEnabled, theme, resetTime }); // Include resetTime in update
    }
  };

  useEffect(() => {
    handleUpdateSettings();
  }, [notificationsEnabled, theme, resetTime]); // Add resetTime to dependencies

  const handleExportData = () => {
    // Logic to handle data export
    console.log("Exporting data...");
  };

  const handleResetData = async () => {
    // Logic to handle data reset
    console.log("Resetting data...");
    await resetSettings(); // Call the resetSettings function
    setSettings(null); // Clear settings after reset
  };

  return (
    <div className="settings-page">
      <h1 className="font-heading text-2xl">Settings</h1>
      <div className="flex flex-col gap-4">
        <TimePicker 
          label="Daily Habit Reset Time" 
          value={resetTime} 
          onChange={handleResetTimeChange} 
        />
        <ReminderSettings habits={habitStore.getAll()} />
        <div className="flex items-center">
          <label className="mr-2 text-text">Enable Notifications:</label>
          <input 
            type="checkbox" 
            checked={notificationsEnabled}
            onChange={(e) => handleToggleNotifications(e.target.checked)} 
            className="toggle-checkbox"
          />
        </div>
        <div className="flex flex-col gap-2">
          <button onClick={handleExportData} className="bg-primary text-white rounded-md p-2">
            Export Data
          </button>
          <button onClick={handleResetData} className="bg-danger text-white rounded-md p-2">
            Reset Data
          </button>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <label htmlFor="theme" className="text-sm font-medium text-text">
            Theme
          </label>
          <select
            id="theme"
            value={theme}
            onChange={(e) => handleThemeChange(e.target.value)}
            className="mt-1 block w-full border border-border rounded-md p-2"
          >
            {THEME_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
  resetSettings,
  updateSettings,
  type SettingsResponse,
  type SettingsUpdate,
} from "../src/lib/settingsClient";
import ReminderSettings from "./ReminderSettings";
import TimePicker from "./TimePicker"; // Importing the new TimePicker component

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
 * resetting preferences and a link out to the existing per-habit
 * ReminderSettings component so reminder scheduling stays configurable
 * from the same place.
 */
export default function SettingsPage() {
  const [settings, setSettings] = useState<SettingsResponse | null>(
    getCachedSettings()
  );
  const [loadState, setLoadState] = useState<LoadState>(
    settings ? "ready" : "loading"
  );
  const [resetTime, setResetTime] = useState<string>("08:00"); // Default reset time
  const [notificationsEnabled, setNotificationsEnabled] = useState<boolean>(false); // State for notifications
  const [theme, setTheme] = useState<string>("light"); // Default theme

  useEffect(() => {
    if (loadState === "loading") {
      fetchSettings().then((fetchedSettings) => {
        setSettings(fetchedSettings);
        setLoadState("ready");
        setTheme(fetchedSettings.theme || "light"); // Set theme from fetched settings or default to light
      }).catch(() => {
        setLoadState("error");
      });
    }
  }, [loadState]);

  const handleResetTimeChange = (time: string) => {
    setResetTime(time);
  };

  const handleToggleNotifications = (enabled: boolean) => {
    setNotificationsEnabled(enabled);
    // Logic to handle enabling/disabling notifications can be added here
  };

  const handleThemeChange = (selectedTheme: string) => {
    setTheme(selectedTheme);
    // Logic to handle theme change can be added here
  };

  const handleUpdateSettings = async () => {
    if (settings) {
      await updateSettings({ notificationsEnabled, theme, resetTime }); // Include resetTime in update
    }
  };

  useEffect(() => {
    handleUpdateSettings();
  }, [notificationsEnabled, theme, resetTime]); // Add resetTime to dependencies

  const handleExportData = () => {
    // Logic to handle data export
    console.log("Exporting data...");
  };

  const handleResetData = async () => {
    // Logic to handle data reset
    console.log("Resetting data...");
    await resetSettings(); // Call the resetSettings function
    setSettings(null); // Clear settings after reset
  };

  return (
    <div className="settings-page">
      <h1 className="font-heading text-2xl">Settings</h1>
      <div className="flex flex-col gap-4">
        <TimePicker 
          label="Daily Habit Reset Time" 
          value={resetTime} 
          onChange={handleResetTimeChange} 
        />
        <ReminderSettings habits={habitStore.getAll()} />
        <div className="flex items-center">
          <label className="mr-2 text-text">Enable Notifications:</label>
          <input 
            type="checkbox" 
            checked={notificationsEnabled}
            onChange={(e) => handleToggleNotifications(e.target.checked)} 
            className="toggle-checkbox"
          />
        </div>
        <div className="flex flex-col gap-2">
          <button onClick={handleExportData} className="bg-primary text-white rounded-md p-2">
            Export Data
          </button>
          <button onClick={handleResetData} className="bg-danger text-white rounded-md p-2">
            Reset Data
          </button>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <label htmlFor="theme" className="text-sm font-medium text-text">
            Theme
          </label>
          <select
            id="theme"
            value={theme}
            onChange={(e) => handleThemeChange(e.target.value)}
            className="mt-1 block w-full border border-border rounded-md p-2"
          >
            {THEME_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}