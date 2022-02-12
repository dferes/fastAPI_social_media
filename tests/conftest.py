from operator import mod
import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL =  f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.test_database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def session():
    '''Drops all tables from the test db, created all tables,
       and yields the db object. Note that if the session fixture 
       is passed as a parameter, we can access the db directly; 
       ie. query the test db'''
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
def client(session):
    '''When client is passed as a parameter into a test, 
       the client fixture will be called, which calls the 
       session fixture before the test for that testing
       function are executed.'''
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db   
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    '''Note that using this fixture will automatically call client, which calls session.
    Though, for access to client or session in a test, we still need to pass it as
    a parameter.
    '''
    user_data = {
        'email':'testemail@gmail.com', 
        'username':'test_user', 
        'password': 'password123'}
    
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    new_user = res.json() 
    new_user['password'] = user_data['password']
    
    return new_user


@pytest.fixture
def test_user2(client):
    '''Creates a user that will be used to verify that an authenticated but
    unauthorized user can't modify or delete other user's posts.
    '''
    user_data = {
        'email':'bad_guy@gmail.com', 
        'username':'bad_guy', 
        'password': 'password123'}
    
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    new_user = res.json() 
    new_user['password'] = user_data['password']
    
    return new_user


@pytest.fixture
def token(test_user):
    '''Creates a JWT for OAuth2'''
    return create_access_token({'username': test_user['username']})


@pytest.fixture
def authorized_client(client, token):
    '''Uses the 'token' fixture and adds the JWT token to the client 
    headers so that protected routes can be accssed.'''
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    '''Creates 3 test posts from test_user and 1 post from test_user2'''
    posts_data = [{
        'title': 'Title 1',
        'content': 'Content 1',
        'username': test_user['username']
    },
    {
        'title': 'Title 2',
         'content': 'Content 2',
         'username': test_user['username']
    },
    {
        'title': 'Title 3',
        'content': 'Content 3',
        'username': test_user['username']
    },
    {
        'title': 'Title 4',
        'content': 'Content 4',
        'username': test_user2['username']
    }]
    
    post_models_list = list(map(lambda post: models.Post(**post), posts_data))
    
    session.add_all(post_models_list)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts


@pytest.fixture
def test_votes(test_user, test_user2, test_posts, session):
    votes_data = [
        {
            'post_id': test_posts[0].id,
            'username': test_user['username'] 
        },
        {
            'post_id': test_posts[0].id,
            'username': test_user2['username']
        }
    ]
    
    vote_models_list = list(map(lambda vote: models.Vote(**vote), votes_data))
    
    session.add_all(vote_models_list)
    session.commit()
    
    votes = session.query(models.Vote).all()
    
    return votes
