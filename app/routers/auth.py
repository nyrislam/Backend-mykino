from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import Session, get_db

router = APIRouter(
    tags=['Authorization']
)

@router.post('/login')
def find_login(login: schemas.UserLogin, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.gmail == login.gmail).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"инвалид")
    if not utils.verify(login.password, get_user.password): # body == db
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"инвалид")
    
    return get_user.username