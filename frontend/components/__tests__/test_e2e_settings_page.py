import os
import pytest
from playwright.sync_api import Page, sync_playwright

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture
def page(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()

def test_settings_page_loads(page: Page):
    page.goto(f"{BASE_URL}/settings")
    assert page.locator("text=Settings").is_visible()
    assert page.locator("text=Loading settings…").is_visible()

def test_settings_page_loads_successfully(page: Page):
    page.goto(f"{BASE_URL}/settings")
    # Simulate successful fetch of settings
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    assert page.locator("text=Settings").is_visible()
    assert page.locator("input[value='light']").is_visible()

def test_change_reset_time(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    page.locator("select[aria-label='Daily Habit Reset Time']").select_option("12:00")
    assert page.locator("select[aria-label='Daily Habit Reset Time']").input_value() == "12:00"

def test_toggle_notifications(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    toggle = page.locator("input[type='checkbox'][aria-label='Enable Notifications:']")
    toggle.check()
    assert toggle.is_checked()

def test_change_theme(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    page.locator("select[aria-label='Theme']").select_option("dark")
    assert page.locator("select[aria-label='Theme']").input_value() == "dark"

def test_export_data(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    page.locator("text=Export Data").click()
    # Here we would check for console output or a network request

def test_reset_data(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    page.locator("text=Reset Data").click()
    # Here we would check for a confirmation or a state change

def test_reset_data_error(page: Page):
    page.goto(f"{BASE_URL}/settings")
    page.evaluate("window.fetch = () => Promise.resolve({ json: () => Promise.resolve({ theme: 'light' }) })")
    page.evaluate("window.resetSettings = () => Promise.reject(new Error('Failed to reset data.'))")
    page.locator("text=Reset Data").click()
    # Here we would check for an error message displayed on the page
    assert page.locator("text=Failed to reset data.").is_visible()