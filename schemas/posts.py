from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    '''' Base Post model for incoming post requests; inherits from pydantic.BaseModel'''
    title: str
    content: str
    published: bool = True # if a default value is provided, the variable is optional
    rating: Optional[int] = None


class PostCreate(PostBase):
    '''Model used for validating PUT requests'''
    pass


class PostResponse(PostBase):
    '''Model used for validating Post responses'''
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True # orm_mode = true will tell the pydantic model to read the data 
                        # even if it is not a 'dict', but an ORM model (or any other 
                        # arbitrary object with attributes) 
                        # Basically, it converts a SQLAlchemy model into a Pydantic model

