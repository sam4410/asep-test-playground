from sqlalchemy import Column, Integer, String, Float
from db.database import Base  # Ensure the correct import path is used

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    questions = relationship("Question", back_populates="quiz")
    teacher = relationship("Teacher")

class Question(Base):
    __tablename__ = 'questions'


    questions = relationship("Question", back_populates="quiz")
    teacher = relationship("Teacher")

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    text = Column(String)
    correct_answer_id = Column(Integer, ForeignKey('answers.id'))

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    text = Column(String)

    question = relationship("Question", back_populates="answers")
