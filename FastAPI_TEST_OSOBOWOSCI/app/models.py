from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .database import Base

class TimestampMixin:
    @declared_attr
    def CreateDate(cls):
        return Column(DateTime, default=func.now(), nullable=False)
    
    # @declared_attr
    # def UpdateDate(cls):
    #     return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Question(Base):
    __tablename__ = "Question"
    QuestionId = Column(Integer,primary_key=True,index=True)
    Content = Column(String)

    answer = relationship("Answer",back_populates="question")


class Mark(Base):
    __tablename__ = "Mark"
    MarkId = Column(Integer, primary_key=True, index=True)
    MarkSign = Column(String)
    Content = Column(String)

    answer = relationship("Answer",back_populates="mark")


class Answer(Base):
    __tablename__ = "Answer"
    AnswerId = Column(Integer, primary_key=True, index=True)
    Content = Column(String)
    QuestionId = Column(Integer, ForeignKey("Question.QuestionId"))
    MarkId = Column(Integer, ForeignKey("Mark.MarkId"))

    question = relationship(Question, back_populates="answer")
    mark = relationship(Mark, back_populates="answer")
 

class Personalities(Base):
    __tablename__ = "Personalities"
    PersonalitiesId = Column(Integer, primary_key=True, index=True)
    Symbol = Column(String)
    Name = Column(String)
    Content = Column(String)
    

    form = relationship("Form", back_populates="personalities")

class Form(Base, TimestampMixin):
    __tablename__ = "Form"
    FormId = Column(Integer, primary_key=True, index=True)
    Answers = Column(String)
    UserName = Column(String)
    PersonalitiesId = Column(Integer, ForeignKey("Personalities.PersonalitiesId"))

    personalities = relationship("Personalities", back_populates="form")


def drop_selected_tables(engine, tables_to_drop):
    """
    Usuń tylko wybrane tabele.
    
    :param engine: Silnik bazy danych.
    :param tables_to_drop: Lista nazw tabel do usunięcia.
    """
    # Pobierz obiekty tabel na podstawie nazw
    selected_tables = [
        table for table in Base.metadata.sorted_tables if table.name in tables_to_drop
    ]
    if not selected_tables:
        print("Brak tabel do usunięcia.")
        return


