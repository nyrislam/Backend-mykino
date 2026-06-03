from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import psycopg2
from psycopg2.extras import RealDictCursor 
from fastapi.middleware.cors import CORSMiddleware
import time
from . import models
from .database import engine, SessionLocal, Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # "*" означает, что мы разрешаем запросы с ЛЮБОГО фронтенда (удобно для локальной разработки)
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"], # Разрешаем любые заголовки
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

try:
    conn = psycopg2.connect(host='localhost', database="fastapi", user="postgres", password="", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("BD connected")
except Exception as error:
    print(error)
    time.sleep(1)


class Register(BaseModel):
    username: str
    gmail: EmailStr
    password: str

class Login(BaseModel):
    gmail: EmailStr
    password: str

@app.get('/')
def get():
    cursor.execute("""SELECT * FROM users""")
    users = cursor.fetchall()
    return {'data': users}

@app.get('/sqlalchemy')
def test(db: Session = Depends(get_db)):
    return {'data': users}

@app.post('/users')
def post_user(reg: Register, status_code=status.HTTP_201_CREATED):
    cursor.execute("""INSERT INTO users (username, gmail, password) VALUES (%s, %s, %s) RETURNING *""", (reg.username, reg.gmail, reg.password))
    users = cursor.fetchone()
    conn.commit()
    return {'data': users}

@app.post('/users/{id}')
def post_user(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s""", (str(id),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    return {'data': user} 

@app.delete('/users/{id}')
def delete_user(id: int):
    cursor.execute("""DELETE FROM users WHERE id = %s RETURNING *""", (str(id),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    conn.commit()
    return {'data': user}

@app.put('/users/{id}')
def put_user(id: int, reg: Register):
    cursor.execute("""UPDATE users SET username=%s, gmail=%s, password=%s WHERE id = %s RETURNING *""", (reg.username, reg.gmail, reg.password, str(id),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    conn.commit()
    return {'data': user}

@app.post('/login')
def find_login(login: Login):
    cursor.execute("""SELECT * FROM users WHERE gmail = %s AND password = %s""", (login.gmail, login.password))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED")
    return {'data': user}