from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean, String
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, ForeignKey('users.username', ondelete='cascade'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published= Column(Boolean, default=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    owner = relationship('User') # This relationship will automatically include all user data associated with the username
    
    
class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = 'votes'
    
    username = Column(String, ForeignKey('users.username', ondelete='cascade'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='cascade'), primary_key=True)    
