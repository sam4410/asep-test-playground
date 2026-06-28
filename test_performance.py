import pytest

# The application may depend on Flask, which might not be installed in the execution
# environment for these tests. If the import fails, we skip the performance test
# rather than erroring out.
try:
    from app import app
except ImportError:  # pragma: no cover
    pytest.skip("Flask or the application could not be imported; skipping performance tests", allow_module_level=True)
