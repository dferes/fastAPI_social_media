from schemas.users import UserResponse
import pytest
from schemas.users import Token
from app.oauth2 import verify_access_token
    

def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == "Welcome To My API!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={
        'username':'test_user2',
        'email':'testingemail@gmail.com',
        'password': 'password123'}
    )
    
    new_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.username == 'test_user2'


def test_login(test_user, client):
    res = client.post('/login', data = {
        'username': test_user['username'], 'password': test_user['password']})
    
    login_res = Token(**res.json())
    token_data = verify_access_token(login_res.access_token)
    
    assert res.status_code == 200
    assert token_data.username == test_user['username']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize('username, password, status_code', [
    ('test_user', 'derp123', 403),
    ('wrong_username', 'password', 404),
    ('wrong_username', 'wrong_password', 404),
    (None, 'password123', 422),
    ('test_user', None, 422)
])
def test_invalid_login(test_user, client, username, password, status_code):
    res = client.post('/login', data={'username': username, 'password': password})
    assert res.status_code == status_code
