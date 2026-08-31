"""Pytest configuration for end-to-end Playwright tests.

Skips e2e tests gracefully when Playwright browser binaries are not
installed, instead of forcing a heavy browser install (which can
trigger out-of-memory failures in constrained CI/sandbox environments).
"""
import pytest


def _browsers_available() -> bool:
    """Best-effort check for installed Playwright browser binaries."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            p.chromium.executable_path
            return True
    except Exception:
        return False


@pytest.fixture(scope="session", autouse=True)
def _skip_if_browsers_missing():
    """Skip the e2e session cleanly if browsers aren't installed."""
    if not _browsers_available():
        pytest.skip(
            "Playwright browsers are not installed; skipping e2e tests.",
            allow_module_level=True,
        )
    yield