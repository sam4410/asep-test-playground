import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="module")
def setup(page: Page):
    # Navigate to the application
    page.goto("http://localhost:8000")
    yield page

def test_dashboard_display(setup):
    page = setup
    # Check if the dashboard displays total spend
    assert page.locator("text=Total Spend").is_visible()

def test_add_transaction(setup):
    page = setup
    # Simulate adding a transaction
    page.fill("input[name='amount']", "1000")  # Amount in cents
    page.select_option("select[name='category']", "Food")
    page.fill("input[name='date']", "2023-10-01")
    page.fill("textarea[name='note']", "Grocery shopping")
    page.click("button[type='submit']")
    assert page.locator("text=Transaction added").is_visible()
