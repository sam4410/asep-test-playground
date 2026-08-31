"""
End-to-end tests for the Settings page user-facing flow.

Covers: navigating to /settings, viewing loaded preferences, updating
theme/language/timezone, toggling notification switches, and using the
danger-zone reset flow. Backend endpoints are mocked at the network layer
via Playwright route interception so these tests are deterministic and do
not require a live backend implementation.

NOTE on memory constraints: in resource-limited CI/sandbox environments the
Playwright Node driver process itself can abort with a V8 "Fatal process out
of memory: Failed to reserve virtual memory for CodeRange" error during
startup, before any browser is launched. This is a failure to reserve the
V8 CodeRange *virtual memory region*, not an old-space heap exhaustion, so
shrinking `--max-old-space-size` alone does not help. The reliable
workaround is to run the Node driver in `--jitless` mode via NODE_OPTIONS,
which disables the JIT (TurboFan/Sparkplug) and therefore avoids allocating
the large CodeRange virtual memory reservation entirely. This must be set
before the driver subprocess is spawned (i.e. before the `playwright`
fixture starts), so we set it at module import time.
"""

import os
import re

import pytest
from playwright.sync_api import Page, expect

# Avoid V8 CodeRange virtual-memory reservation failures in constrained
# sandboxes/containers by running the Node driver process JIT-less. This
# must be set before the playwright driver subprocess is spawned.
os.environ["NODE_OPTIONS"] = " ".join(
    filter(
        None,
        [os.environ.get("NODE_OPTIONS", ""), "--jitless"],
    )
).strip()

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

DEFAULT_SETTINGS = {
    "id": "settings-1",
    "user_id": "user-1",
    "theme": "light",
    "language": "en",
    "email_notifications": True,
    "push_notifications": False,
    "timezone": "UTC",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

RESET_SETTINGS = {
    **DEFAULT_SETTINGS,
    "theme": "system",
    "language": "en",
    "email_notifications": True,
    "push_notifications": False,
    "timezone": "UTC",
    "updated_at": "2024-01-02T00:00:00Z",
}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Reduce browser (not driver) memory footprint to avoid OOM in constrained sandboxes."""
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-gpu",
        ],
    }


def _mock_settings_routes(page: Page, state: dict) -> None:
    """Intercept /settings API calls and serve/update an in-memory state dict."""

    def handle_settings(route):
        request = route.request
        if request.method == "GET":
            route.fulfill(status=200, json=state)
        elif request.method in ("PATCH", "PUT"):
            import json as _json

            body = _json.loads(request.post_data() or "{}")
            state.update(body)
            route.fulfill(status=200, json=state)
        else:
            route.continue_()

    def handle_reset(route):
        state.clear()
        state.update(RESET_SETTINGS)
        route.fulfill(status=200, json=state)

    page.route(re.compile(r".*/settings$"), handle_settings)
    page.route(re.compile(r".*/settings/reset$"), handle_reset)


def test_settings_page_loads_and_displays_preferences(page: Page):
    state = dict(DEFAULT_SETTINGS)
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    expect(page.get_by_role("heading", name="Settings")).toBeVisible()
    expect(page.get_by_label("Theme")).toHaveValue("light")
    expect(page.get_by_label("Language")).toHaveValue("en")
    expect(page.get_by_label("Timezone")).toHaveValue("UTC")


def test_user_can_update_theme_preference(page: Page):
    state = dict(DEFAULT_SETTINGS)
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    theme_select = page.get_by_label("Theme")
    expect(theme_select).toBeVisible()

    theme_select.select_option("dark")

    expect(theme_select).toHaveValue("dark")
    assert state["theme"] == "dark"


def test_user_can_update_language_preference(page: Page):
    state = dict(DEFAULT_SETTINGS)
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    language_select = page.get_by_label("Language")
    language_select.select_option("es")

    expect(language_select).toHaveValue("es")
    assert state["language"] == "es"


def test_user_can_update_timezone_on_blur(page: Page):
    state = dict(DEFAULT_SETTINGS)
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    timezone_input = page.get_by_label("Timezone")
    timezone_input.fill("America/New_York")
    # Trigger blur by focusing elsewhere
    page.get_by_role("heading", name="Settings").click()

    expect(timezone_input).toHaveValue("America/New_York")
    assert state["timezone"] == "America/New_York"


def test_user_can_toggle_email_notifications(page: Page):
    state = dict(DEFAULT_SETTINGS)
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    email_toggle = page.get_by_role("switch", name=re.compile("Email notifications", re.I))
    expect(email_toggle).toBeVisible()

    initial_checked = email_toggle.get_attribute("aria-checked") == "true"
    email_toggle.click()

    expect(email_toggle).toHaveAttribute(
        "aria-checked", "false" if initial_checked else "true"
    )
    assert state["email_notifications"] != initial_checked


def test_settings_error_state_is_shown_when_load_fails(page: Page):
    def handle_settings_error(route):
        route.fulfill(status=500, json={"detail": "Internal Server Error"})

    page.route(re.compile(r".*/settings$"), handle_settings_error)

    page.goto(f"{BASE_URL}/settings")

    expect(page.get_by_text(re.compile("couldn't load settings", re.I))).toBeVisible()


def test_user_can_reset_settings_to_defaults(page: Page):
    state = dict(DEFAULT_SETTINGS)
    state["theme"] = "dark"
    state["timezone"] = "America/New_York"
    _mock_settings_routes(page, state)

    page.goto(f"{BASE_URL}/settings")

    reset_button = page.get_by_role("button", name=re.compile("reset", re.I))
    expect(reset_button).toBeVisible()
    reset_button.click()

    # Confirm the reset action if a confirmation control appears
    confirm_button = page.get_by_role("button", name=re.compile("confirm|yes", re.I))
    if confirm_button.count() > 0:
        confirm_button.first.click()

    expect(page.get_by_label("Theme")).toHaveValue("system")
    expect(page.get_by_label("Timezone")).toHaveValue("UTC")