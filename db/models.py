from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, category='{self.category}', date='{self.date}', user_id={self.user_id})>"
