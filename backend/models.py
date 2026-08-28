from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_user_id = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, clerk_user_id={self.clerk_user_id})>"

    # Additional fields can be added here as needed
    # e.g., name = Column(String), email = Column(String)
    # Ensure to update the database schema accordingly when adding new fields.