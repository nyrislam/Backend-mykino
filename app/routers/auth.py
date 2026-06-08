from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import Session, get_db

router = APIRouter(
    tags=['Authorization']
)

@router.post('/login')
def find_login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.email == login.username).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"инвалид")
    if not utils.verify(login.password, get_user.password): # body == db
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"инвалид")
    
    access_token = oauth2.create_access_token(data={"user_id": get_user.id})

    return {"access_token": access_token, "token_type": "bearer"}
