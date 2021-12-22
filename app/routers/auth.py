from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from schemas.users import UserLogin
from .. import models, utils, database


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(database.get_db)):        
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with the username: {user_credentials.username} exists.')
    
    if not utils.verify_user(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials') 
    return {''}
