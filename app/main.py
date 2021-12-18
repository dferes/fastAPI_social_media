from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from schemas.posts import Post
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
 
app = FastAPI()


my_posts = [
    {
        'id': 1,
        'title': 'Title 1',
        'content': 'Look, my first post'
    },
    {
        'id': 2,
        'title': 'Title 2',
        'content': 'Look, another post'
    }
]

# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {'data': posts}    


@app.get('/')
def root():
    return {'message': 'Welcome to my api!!!'}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'posts': posts}


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return { 'post': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict()) # illegal syntax...but it works for now. Consider making a function for this.     
    db.add(new_post)
    db.commit()
    db.refresh(new_post
               )
    return {'data':new_post}     


@app.put('/posts/{id}')
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    
    return {'data': post_query.first()}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        
    post.delete(synchronize_session=False) # Look this up again. Forgot how it works.
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)