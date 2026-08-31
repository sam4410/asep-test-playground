"""Pytest configuration for end-to-end Playwright tests.

Skips e2e tests gracefully when Playwright browser binaries are not
installed, instead of forcing a heavy browser install (which can
trigger out-of-memory failures in constrained CI/sandbox environments).
"""
import os
import pytest


def _browsers_available() -> bool:
    """Best-effort check for installed Playwright browser binaries.

    Merely referencing ``executable_path`` does not verify the browser
    binary is actually present on disk, so we perform a real (cheap)
    launch/close cycle to confirm the binary exists and is runnable.
    """
    # Allow explicitly disabling e2e browser checks in environments where
    # even a launch/close probe is undesirable (e.g. memory-constrained CI).
    if os.environ.get("SKIP_E2E_BROWSER_CHECK") == "1":
        return False
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
            return True
    except Exception:
        return False


@pytest.fixture(scope="session", autouse=True)
def _skip_if_browsers_missing():  # noqa: D401 - fixture docstring below
    """Skip the e2e session cleanly if browsers aren't installed."""
    if not _browsers_available():
        pytest.skip(            "Playwright browsers are not installed; skipping e2e tests.",
            allow_module_level=True,
        )
    yield