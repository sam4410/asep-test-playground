from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_user_id = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, clerk_user_id={self.clerk_user_id})>"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    client_name = Column(String, index=True)
    amount = Column(Integer)
    status = Column(String)  # 'paid' or 'unpaid'