from pydantic import BaseModel 

class Question(BaseModel):
    QuestionId : int
    Content : str 

class Answer(BaseModel):
    AnswerId : int 
    QuestionId : int
    Content : str
    MarkId : int

class AnswerWithMark(BaseModel):
    AnswerId : int 
    QuestionId : int
    Content : str
    MarkSign : str
    
class AllAnswers(BaseModel):
    Answers : list [Answer]

class AllQuestions(BaseModel):
    Questions : list [Question]

class FullQuestion(BaseModel):
    Answers: list[AnswerWithMark] 

class AnswerList(BaseModel):
    Answers: list [Answer]

class Mark(BaseModel):
    MarkSign : str
    Content : str

class FormCreate(BaseModel):
    Answers: str
    UserName: str
    PersonalitiesId: int

class FormResponse(BaseModel):
    FormId: int
    Answers: str
    UserName: str
    PersonalitiesId: int

    class Config:
        from_attributes = True

class Personality(BaseModel):
    PersonalitiesId: int
    Symbol: str
    Name: str
    Content: str
    