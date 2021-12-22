from datetime import datetime
from pydantic.main import BaseModel
from pydantic import BaseModel
# from typing import Optional
from datetime import datetime
from pydantic.networks import EmailStr


class UserCreate(BaseModel):
    '''Pydantic model for validating request body for creating users'''
    username: str
    email: EmailStr  # Validator for email format/shape
    password: str
    
    
class UserResponse(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
