from fastapi import status, HTTPException, Depends, APIRouter
from schemas.users import UserCreate, UserResponse
from .. import models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']                   
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
               
    return new_user


@router.get('/{username}', response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db), user_: str = Depends(oauth2.get_current_user)):
    # decide on using the code below or the variable from the Depends(oauth2) above
    # for getting the user data. Redundant as it is now.
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with the username {username} exists.')
    
    return user
