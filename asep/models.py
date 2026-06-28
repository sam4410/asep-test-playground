"""
Database models for the ASEP authentication system.

The project currently uses FastAPI; SQLAlchemy is the de‑facto ORM for such
applications.  These models define:
* **User** – stores account information, a hashed password and a role.
* **RefreshToken** – stores long‑lived refresh tokens linked to a user.
* **RevokedToken** – a simple revocation list for JWT access tokens that have
  been explicitly invalidated (e.g., on logout or password change).

The models are deliberately minimal – they can be extended later without
affecting the existing API endpoints.
"""

from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents an application user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    # Store a bcrypt/argon2 hash, never the plain password.
    password_hash = Column(String(255), nullable=False)
    # Role can be 'admin' or 'user' (regular).  Stored as plain text for simplicity.
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to refresh tokens
    refresh_tokens: List["RefreshToken"] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id} email={self.email} role={self.role}>"


class RefreshToken(Base):
    """
    Stores a refresh token that can be exchanged for a new access JWT.
    The token itself is stored hashed (e.g., using SHA‑256) to avoid leaking
    raw token values if the DB is compromised.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Hashed token value
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    # When the token expires
    expires_at = Column(DateTime, nullable=False)
    # Optional revocation flag (soft delete)
    revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user: User = relationship("User", back_populates="refresh_tokens")

    def is_valid(self) -> bool:
        """Return True if the token is not revoked and not expired."""
        return not self.revoked and self.expires_at > datetime.utcnow()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RefreshToken id={self.id} user_id={self.user_id} revoked={self.revoked}>"


class RevokedToken(Base):
    """
    Simple revocation list for JWT access tokens.
    Storing the jti (JWT ID) allows quick lookup to reject a token that has
    been explicitly invalidated before its natural expiry.
    """
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    revoked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Index to efficiently purge expired entries
    __table_args__ = (Index("ix_revoked_tokens_expires_at", "expires_at"),)

    def is_expired(self) -> bool:
        return self.expires_at <= datetime.utcnow()

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RevokedToken jti={self.jti}>"

# Helper function to create a hash of a raw refresh token.
# The actual hashing implementation (e.g., hashlib.sha256) should be used
# wherever tokens are generated/validated.
def hash_refresh_token(raw_token: str) -> str:
    import hashlib

    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

# Example utility to generate a new refresh token (not persisted here)
def generate_refresh_token(user_id: int, expires_in: timedelta = timedelta(days=30)) -> dict:
    """
    Returns a dict with the raw token (to be sent to the client) and a
    RefreshToken instance ready to be added to the session.
    """
    import secrets

    raw = secrets.token_urlsafe(48)
    token_hash = hash_refresh_token(raw)
    expires_at = datetime.utcnow() + expires_in
    token_obj = RefreshToken(
        user_id=user_id, token_hash=token_hash, expires_at=expires_at, revoked=False
    )
    return {"raw_token": raw, "token_obj": token_obj}
