from pydantic import BaseModel, EmailStr, conint, validator
from datetime import datetime
from typing import  Optional
from pydantic.types import conint

# class Post(BaseModel):
#     title:str
#     content:str
#     published: bool = True 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # ------
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # It works for me whithout this (posibly b/c of updated versions)
    class Config:
        orm_mode = True

class PostOut(BaseModel):
     Post: Post
     votes:int

     class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: int
    @validator('dir')
    def check_value(cls, v):
                if v > 1:
                    raise ValueError('value must be less than or equal to 1')
                return v

