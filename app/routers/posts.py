from fastapi import Response, status, HTTPException, Depends, APIRouter
from schemas.posts import PostCreate, PostResponse, PostVoteResponse
from .. import models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user),
limit: int = 10, owner: str = None, skip: int = 0, search: Optional[str] = ''):    
    # Look at SQLAlchemy docs to clean this up. Super redundant
    if owner:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search), models.Post.username == current_user.username).limit(limit).offset(skip).all() # By default, left inner join
    else:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all() # By default, left inner join
    
    return posts


@router.get('/{id}', response_model=PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), user: str = Depends(oauth2.get_current_user)):
    new_post = models.Post(username=user.username, **post.dict()) # unpacking syntax 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post     


@router.put('/{id}', response_model=PostResponse)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), 
current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
        
    if post.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                   
                            detail=f'post with id: {id} not found')
    if post.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
