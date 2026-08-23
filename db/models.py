from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # Adjusted import to use absolute path
from .user import User  # Added import for User model

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
