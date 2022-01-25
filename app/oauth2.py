from fastapi.param_functions import Depends
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from schemas.users import TokenData
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # this line is throwing error...wtf
    
        username: str = payload.get('username')

        if username is None: raise credentials_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception 
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''Ensures that a user is logged in, not that an AUTHORIZED user is logged in''' 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials.', 
                                          headers={'WWW-Authenticate': 'Bearer'} )
    
    token = verify_access_token(token, credentials_exception)
    # throw error here if no user found ..
    user = db.query(models.User).filter(models.User.username == token.username).first()
    
    return user



# Probably best to use middleware for the code below

# def ensure_authorized_user(username: str, token: str = Depends(oauth2_scheme)):
#     token_data = get_current_user(token)
    
#     if token_data.username != username:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                           detail='Forbidden.', 
#                                           headers={'WWW-Authenticate': 'Bearer'} )
#     return True