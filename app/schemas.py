from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str
    
class UserLogin(UserBase):
    password: str

class Resp(UserBase):
    id: int
    username: str
    class Config:
        from_attributes=True