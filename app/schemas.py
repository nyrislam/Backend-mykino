from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str
    
class UserLogin(UserBase):
    password: str

class UserResp(UserBase):
    id: int
    username: str
    class Config:
        from_attributes=True


class WishlistBase(BaseModel):
    kinopoiskId: int
    name: str
    posterUrl: str
    # owner_id: int

class WishlistResp(WishlistBase):
    class Config:
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
