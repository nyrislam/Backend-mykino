from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from . import models
from .database import engine, Session, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Register(BaseModel):
    username: str
    gmail: EmailStr
    password: str

class Login(BaseModel):
    gmail: EmailStr
    password: str

@app.get('/')
def test(db: Session = Depends(get_db)):
    res = db.query(models.User).all()
    return {'data': res}

@app.post('/users')
def post_user():
    return