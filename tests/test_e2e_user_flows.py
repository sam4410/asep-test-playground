import os
import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("page_url", [
    "/login",
    "/signup",
    "/dashboard",
    "/feature"
])
def test_page_loads(page: Page, page_url):
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    page.goto(f"{base_url}{page_url}")
    assert page.title() != ""

def test_login_flow(page: Page):
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    page.goto(f"{base_url}/login")
    
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    
    page.wait_for_url(f"{base_url}/dashboard")
    assert page.locator("text=Welcome to your dashboard!").is_visible()

def test_signup_flow(page: Page):
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    page.goto(f"{base_url}/signup")
    
    page.fill('input[name="username"]', 'newuser')
    page.fill('input[name="email"]', 'newuser@example.com')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    
    page.wait_for_url(f"{base_url}/dashboard")
    assert page.locator("text=Welcome to your dashboard!").is_visible()

def test_flash_message_display(page: Page):
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    page.goto(f"{base_url}/login")
    page.evaluate("flash('This is a test message.')")
    page.reload()
    assert page.locator("text=This is a test message.").is_visible()