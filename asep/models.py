"""
SQLAlchemy models defining the persistence layer for authentication.
Includes:
* User – stores credentials, role and basic profile information.
* RefreshToken – stores issued refresh tokens linked to a user with expiry.

These models are deliberately simple to keep the example focused on the
authentication flow. In a production system you would add indexes,
password hashing, audit fields, etc.
"""

from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    Enum as SQLEnum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    Represents an application user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    # In a real app store a password hash, not plain text.
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False, default=RoleEnum.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to refresh tokens
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id} email={self.email} role={self.role}>"


class RefreshToken(Base):
    """
    Stores a refresh token issued to a user.
    The token itself is a UUID string; we store its hash in the DB for
    additional security in a real deployment.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        UniqueConstraint("token", name="uq_refresh_token_token"),
    )

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RefreshToken id={self.id} user_id={self.user_id} expires={self.expires_at}>"

    @staticmethod
    def default_expiry() -> datetime:
        """Convenient helper to compute the default expiry datetime."""
        return datetime.utcnow() + timedelta(days=7)