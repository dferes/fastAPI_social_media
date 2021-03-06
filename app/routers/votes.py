from email.policy import HTTP
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import database, models, oauth2
from schemas.votes import Vote


router = APIRouter(
    prefix='/votes',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote: Vote, response: Response, db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {vote.post_id} does not exist')
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.username == current_user.username) # composite key
    
    found_vote = vote_query.first()
    
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.username} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, username=current_user.username)
        db.add(new_vote)
        db.commit()
        
        return {'message': 'Successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        
        return {'message': 'successfully deleted vote'}  
