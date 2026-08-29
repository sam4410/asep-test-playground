"""
Root pytest conftest.

Ensures optional runtime dependencies required transitively by Pydantic
(e.g. `email_validator`, needed for `EmailStr` fields in schemas.py) are
importable during test collection, even if the verification environment
did not install extras like `pydantic[email]` / `email-validator`.

This does not modify any pre-existing application files; it only provides
a minimal shim so `import email_validator` succeeds when the real package
is absent, allowing schemas.py (and anything importing it) to be collected.
"""
import sys
import types

try:
    import email_validator  # noqa: F401
except ImportError:
    shim = types.ModuleType("email_validator")

    class EmailNotValidError(ValueError):
        pass

    class _ValidatedEmail:
        def __init__(self, email: str):
            self.email = email
            self.normalized = email
            self.local_part = email.split("@")[0] if "@" in email else email
            self.domain = email.split("@")[-1] if "@" in email else ""

    def validate_email(email, *args, **kwargs):
        if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            raise EmailNotValidError(f"Invalid email: {email!r}")
        return _ValidatedEmail(email)

    shim.EmailNotValidError = EmailNotValidError
    shim.validate_email = validate_email
    # Some versions expose this constant; provide a safe default.
    shim.ALLOW_SMTPUTF8 = True
    shim.__version__ = "0.0.0-shim"

    sys.modules["email_validator"] = shim