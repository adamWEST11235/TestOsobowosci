import pandas as pd 
from sqlalchemy import text
from sqlalchemy.orm import Session
from pathlib import Path

from app import  models

file_name = 'data.xlsx'
current_folder = Path(__file__).parent
file_path = current_folder / file_name  # Połącz ścieżkę z nazwą pliku


def update_marks(db: Session, file_path, sheet_name = "marks"):
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name)

    except Exception as e:
        print(f"Error reading the Excel sheet: {e}")
        return None
    
    for index, row in data.iterrows():

        new_mark = models.Mark(
            MarkSign = row['MarkSign'],
            Content = row['Content']
        )
        db.add(new_mark)
        db.commit()
        db.refresh(new_mark)
    return None

def update_personalities(db: Session, file_path, sheet_name = "personalities"):
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name)

    except Exception as e:
        print(f"Error reading the Excel sheet: {e}")
        return None
    
    for index, row in data.iterrows():

        new_personalitiy = models.Personalities(
            Symbol = row['Symbol'],
            Name = row['Name'],
            Content = row['Content']
        )
        db.add(new_personalitiy)
        db.commit()
        db.refresh(new_personalitiy)
    return None

def update_question(db: Session, content):
    new_questuon = models.Question(
        Content=content
    )
    db.add(new_questuon)
    db.commit()
    db.refresh(new_questuon)
    
    return new_questuon.QuestionId

def update_answer(db: Session, content, question_id, mark_id  ):
    new_answer = models.Answer(
        Content = content,
        QuestionId = question_id,
        MarkId = mark_id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def update_test(db: Session):
    update_marks(db, file_path)
    update_personalities(db, file_path)

    data = pd.read_excel(file_path, sheet_name="questions")

    for index, row in data.iterrows():
        question_id = update_question(db, row['Question'])

        mark1 = db.query(models.Mark).filter(models.Mark.MarkSign == row['MarkSign1']).first()
        mark2 = db.query(models.Mark).filter(models.Mark.MarkSign == row['MarkSign2']).first()
        update_answer(db, row['Answer1'], question_id, mark1.MarkId)
        update_answer(db, row['Answer2'], question_id, mark2.MarkId)

        

   

