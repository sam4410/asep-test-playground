import os
import pytest
from components.SettingsPage import SettingsPage
from lib.settingsClient import fetchSettings, updateSettings, resetSettings

@pytest.fixture
def settings_page():
    return SettingsPage()

def test_handle_reset_time_change(settings_page):
    settings_page.handleResetTimeChange("12:00")
    assert settings_page.resetTime == "12:00"

def test_handle_toggle_notifications(settings_page):
    settings_page.handleToggleNotifications(True)
    assert settings_page.notificationsEnabled is True
    settings_page.handleToggleNotifications(False)
    assert settings_page.notificationsEnabled is False

def test_handle_theme_change(settings_page):
    settings_page.handleThemeChange("dark")
    assert settings_page.theme == "dark"
    settings_page.handleThemeChange("light")
    assert settings_page.theme == "light"

def test_handle_update_settings(settings_page, mocker):
    mock_update = mocker.patch('lib.settingsClient.updateSettings')
    settings_page.notificationsEnabled = True
    settings_page.theme = "dark"
    settings_page.resetTime = "12:00"
    
    settings_page.handleUpdateSettings()
    
    mock_update.assert_called_once_with({
        'notificationsEnabled': True,
        'theme': 'dark',
        'resetTime': '12:00'
    })

def test_handle_export_data(mocker, capsys):
    mock_print = mocker.patch('builtins.print')
    settings_page.handleExportData()
    mock_print.assert_called_once_with("Exporting data...")

def test_handle_reset_data(mocker, settings_page):
    mock_reset = mocker.patch('lib.settingsClient.resetSettings', return_value=None)
    settings_page.handleResetData()
    mock_reset.assert_called_once()
    assert settings_page.settings is None

def test_handle_reset_data_error(mocker, settings_page):
    mock_reset = mocker.patch('lib.settingsClient.resetSettings', side_effect=Exception("Failed to reset data."))
    with pytest.raises(Exception) as excinfo:
        settings_page.handleResetData()
    assert str(excinfo.value) == "Failed to reset data."
    mock_reset.assert_called_once()