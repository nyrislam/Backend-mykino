from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/wishlists', 
    tags=['Wishlists']
)

@router.get('/', response_model=List[schemas.WishlistResp])
def get_wish(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    res = db.query(models.Wishlist).filter(models.Wishlist.owner_id == current_user.id)
    print(res)
    return res

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.WishlistResp)
def add_wish(reg: schemas.WishlistBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_user = models.Wishlist(owner_id=current_user.id, **reg.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.WishlistResp)
def get_wish(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    wish = db.query(models.Wishlist).filter(models.Wishlist.id == id).first()
    if not wish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    if wish.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorized to perform requested action")
    return wish

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wish(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    wish_query = db.query(models.Wishlist).filter(models.Wishlist.id == id)
    wish = wish_query.first()
    print(wish.owner_id, current_user.id)
    if not wish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user wish id={id}")
    
    if wish.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorized to perform requested action")
    
    # wish.delete(synchronize_session=False)
    # db.commit()
    
    return {'data': "delete"}

@router.put('/{id}', response_model=schemas.WishlistResp)
def put_wish(id: int, reg: schemas.WishlistBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    wish_query = db.query(models.Wishlist).filter(models.Wishlist.id == id)
    wish = wish_query.first()
    if not wish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUNDED user with id={id}")
    
    if wish.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorized to perform requested action")
    # wish.update(reg.dict(), synchronize_session=False)
    # db.commit()
    return wish.first()

