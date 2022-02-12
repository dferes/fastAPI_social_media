from datetime import datetime
from pydantic import BaseModel
from . import users


class PostBase(BaseModel):
    '''' Base Post model for incoming post requests; inherits from pydantic.BaseModel'''
    title: str
    content: str
    published: bool = True # default
    

class PostCreate(PostBase):
    '''Model used for validating PUT requests'''
    pass


class PostResponse(PostBase):
    '''Model used for validating Post responses'''
    id: int
    created_at: datetime
    username: str
    owner: users.UserResponse
    
    class Config:
        orm_mode = True # orm_mode = true will tell the pydantic model to read the data 
                        # even if it is not a 'dict', but an ORM model (or any other 
                        # arbitrary object with attributes) 
                        # Basically, it converts a SQLAlchemy model into a Pydantic model

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int 

    class Config:
        orm_mode = True
