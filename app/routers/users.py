from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, utils
from ..database import Session, get_db

router = APIRouter(
    prefix='/users', 
    tags=['Users']
)

@router.get('/', response_model=List[schemas.Resp])
def get_users(db: Session = Depends(get_db)):
    res = db.query(models.User).all()
    return res

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Resp)
def create_user(reg: schemas.UserCreate, db: Session = Depends(get_db)):
    reg.password = utils.hash(reg.password)
    new_user = models.User(**reg.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.Resp)
def get_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    print(get_user)
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    return get_user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id)
    if not get_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    
    get_user.delete(synchronize_session=False)
    db.commit()
    
    return {'data': "delete"}

@router.put('/{id}', response_model=schemas.Resp)
def put_user(id: int, reg: schemas.UserCreate, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id)
    if not get_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    get_user.update(reg.dict(), synchronize_session=False)
    db.commit()
    return get_user.first()

