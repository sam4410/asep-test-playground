from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.CheckConstraint(
            "email = lower(trim(email))",
            name='ck_users_email_normalized',
        ),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @validates('email')
    def normalize_email(self, key, value):
        if value is None:
            return value
        return value.strip().lower()

    def __repr__(self):
        return f'<User {self.email}>'

    transactions = db.relationship(
        'Transaction',
        back_populates='owner',
        cascade='all, delete-orphan',
    )

class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = (
        db.CheckConstraint(
            "transaction_type IN ('income', 'expense')",
            name='ck_transactions_type',
        ),
        db.CheckConstraint(
            'amount_cents >= 0',
            name='ck_transactions_amount_cents_nonnegative',
        ),
        db.Index('ix_transactions_user_date', 'user_id', 'transaction_date'),
        db.Index('ix_transactions_user_type', 'user_id', 'transaction_type'),
    )

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    amount_cents = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(7), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False, index=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    owner = db.relationship('User', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction {self.id}, {self.transaction_type}, {self.amount_cents}>'

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        if not name:
            raise ValueError("Name cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive float")
        self.name = name
        self.price = price

    def __repr__(self):
        return f'<Product {self.name}, Price: {self.price}>'