from sqlalchemy.orm import Session

from . import models

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.QuestionId == question_id).first()

def get_answer(db: Session, answer_id: int):
    return db.query(models.Answer).filter(models.Answer.AnswerId == answer_id).first()

def get_answers_by_question(db: Session, question_id: int):
    return db.query(models.Answer).join(models.Mark, models.Answer.MarkId == models.Mark.MarkId).filter(models.Answer.QuestionId == question_id)

def get_mark(db: Session, mark_id: int):
    return db.query(models.Mark).filter(models.Mark.MarkId == mark_id).first()

def get_all_questions_id(db: Session):
    return db.query(models.Question)

def get_all_answers(db: Session):
    return db.query(models.Answer)

def get_personality(db: Session, symbol: str):
    return db.query(models.Personalities).filter(models.Personalities.Symbol == symbol).first()