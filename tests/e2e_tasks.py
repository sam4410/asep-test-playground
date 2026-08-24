import os
import pytest
from playwright.sync_api import Page

@pytest.mark.parametrize("username, password", [
    ("testuser", "password123"),
])
def test_task_management_flow(page: Page, username: str, password: str):
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

    # User Signup
    page.goto(f"{base_url}/public/index.html")  # Assuming the frontend is served in the public directory
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.fill("input[name='email']", "test@example.com")
    page.click("button[type='submit']")  # Assuming there's a signup button
    assert page.locator("text=User created successfully").is_visible()

    # User Login
    page.goto(f"{base_url}/public/index.html")  # Redirect to login page
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")  # Assuming there's a login button
    assert page.locator("text=Login successful").is_visible()

    # Create Task
    page.click("text=Create Task")  # Navigate to create task page
    page.fill("input[name='title']", "New Task")
    page.fill("textarea[name='description']", "Task description")
    page.fill("input[name='assignee']", username)
    page.fill("input[name='due_date']", "2023-12-31")
    page.select_option("select[name='status']", "todo")  # Assuming a dropdown for status
    page.click("button[type='submit']")  # Assuming there's a create task button
    assert page.locator("text=Task created successfully").is_visible()

    # Get Tasks
    page.goto(f"{base_url}/public/index.html")  # Redirect to tasks page
    assert page.locator("text=New Task").is_visible()

    # Filter Tasks by Assignee
    page.fill("input[placeholder='Filter by assignee']", username)
    assert page.locator("text=New Task").is_visible()
    assert page.locator("text=Another Task").is_hidden()  # Assuming another task exists
    
    # Activity Log Check
    page.goto(f"{base_url}/public/index.html")  # Redirect to activity log page
    assert page.locator("text=Activity log entry created successfully").is_visible()  # Assuming this is shown somewhere
    
    # Logout (if applicable)
    page.click("text=Logout")  # Assuming there's a logout button
    assert page.locator("text=Login").is_visible()  # Check if redirected to login page