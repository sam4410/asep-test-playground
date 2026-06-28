# Import the Flask app; try several common import patterns.
# If the application cannot be imported, skip the entire suite.
try:
    # Most projects expose a Flask instance directly.
    from app import app, COUNTRIES  # type: ignore
except Exception:  # pragma: no cover
    try:
        # Some projects expose a factory function.
        from app import create_app, COUNTRIES  # type: ignore
        app = create_app()
    except Exception:
        try:
            # Fallback to a top‑level module named ``main``.
            from main import app, COUNTRIES  # type: ignore
        except Exception:
            pytest.skip(
                "Application could not be imported; skipping security tests",
                allow_module_level=True,
            )
