from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from data.update import update_test


from . import crud,models, schema
from .database import SessionLocal, engine, get_db

tables_to_drop=['Question','Mark', 'Answer', 'Personalities']

models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        print("Checking if table is empty...")
        update_test(db)
    finally:
        db.close()

@app.get("/question/{question_id}/",response_model=schema.Question)
def get_question(question_id:int, db:Session=Depends(get_db)):
    db_question = crud.get_question(db,question_id = question_id )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.get("/answer/{answer_id}/",response_model=schema.Answer)
def get_answer(answer_id:int, db:Session=Depends(get_db)):
    db_question = crud.get_answer(db,answer_id = answer_id )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_question

@app.get("/answer_by_question/{question_id}/",response_model=schema.FullQuestion) 
def get_answers_by_question(question_id:int, db:Session=Depends(get_db)):
    db_answer= crud.get_answers_by_question(db,question_id = question_id)

    if (db_answer is None):
        raise HTTPException(status_code=404, detail="Answer by questionId not found")
    return {
        'Answers' : [{'AnswerId': a.AnswerId,'QuestionId' : a.QuestionId  ,'Content' : a.Content,'MarkSign' : a.mark.MarkSign  } for a in db_answer]
    }

@app.get("/mark/{mark_id}/",response_model=schema.Mark)
def get_mark(mark_id:int, db:Session=Depends(get_db)):
    db_question = crud.get_mark(db,mark_id = mark_id )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return db_question


@app.get("/get_all_questions_id/",response_model=schema.AllQuestions)
def get_all_questions_id(db:Session=Depends(get_db)):
    db_question = crud.get_all_questions_id(db)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Questions not found")
    return {'Questions' :[{'QuestionId' : a.QuestionId, 'Content' : a.Content} for a in db_question ]}

@app.get("/get_all_answers/",response_model=schema.AllAnswers)
def get_all_answers(db:Session=Depends(get_db)):
    db_answers = crud.get_all_answers(db)
    if db_answers is None:
        raise HTTPException(status_code=404, detail="Answers not found")
    return {'Answers' :[{'AnswerId' : a.AnswerId,  'QuestionId' : a.QuestionId, 'Content': a.Content, 'MarkId': a.MarkId} for a in db_answers ]}


@app.post("/form/", response_model=schema.FormResponse)
async def create_form(form: schema.FormCreate, db: Session = Depends(get_db)):

    new_form = models.Form(
        Answers=form.Answers,   
        UserName=form.UserName,
        PersonalitiesId=form.PersonalitiesId
    )

    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return new_form

@app.get("/get_personality/{symbol}/", response_model=schema.Personality)
def get_personality(symbol:str, db:Session=Depends(get_db)):
    db_persionality = crud.get_personality(db, symbol = symbol)
    if db_persionality is None:
        raise HTTPException(status_code=404, detail="Personality not found")
    return db_persionality