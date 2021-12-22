from fastapi import status, HTTPException, Depends, APIRouter
from schemas.users import UserCreate, UserResponse
from .. import models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']                   
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # user_check = db.query(models.User).filter(models.User.username == user.dict()['username'])
    # print('----------------------------------------------', user_check)
    # if user_check.first():
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail=f"Username {user.dict()['username']} already taken.")
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
               
    return new_user


@router.get('/{username}', response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with the username {username} exists.')
    
    return user
