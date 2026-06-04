from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from . import models, schemas, utils
from .database import engine, Session, get_db
from .settings import setup_cors

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
setup_cors(app)


@app.get('/users', response_model=List[schemas.Resp])
def get_users(db: Session = Depends(get_db)):
    res = db.query(models.User).all()
    return res

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.Resp)
def create_user(reg: schemas.UserCreate, db: Session = Depends(get_db)):
    reg.password = utils.hash(reg.password)
    new_user = models.User(**reg.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=schemas.Resp)
def get_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    print(get_user)
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    return get_user

@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id)
    if not get_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    
    get_user.delete(synchronize_session=False)
    db.commit()
    
    return {'data': "delete"}

@app.put('/users/{id}', response_model=schemas.Resp)
def put_user(id: int, reg: schemas.UserCreate, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id)
    if not get_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    get_user.update(reg.dict(), synchronize_session=False)
    db.commit()
    return get_user.first()


@app.post('/login', response_model=schemas.Resp)
def find_login(login: schemas.UserLogin, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.gmail == login.gmail, models.User.password == login.password).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED")
    return get_user