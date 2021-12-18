from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if a default value is provided, the variable is optional
    rating: Optional[int] = None
