from schemas.posts import PostResponse
from schemas.users import Token
import pytest

from tests.conftest import authorized_client


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    post_response_list = list(map(lambda post: PostResponse(**post["Post"]), res.json()))
    assert res.status_code == 200
    assert len(post_response_list) == len(test_posts)
    
# TODO:
#   for the get all posts endpoint, don't forget to test all possible 
#   combinatinos of filter options: 
#       .limit
#       .owner
#       .skip
#       .search 

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401
 
 
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_get_one_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/1000')
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = PostResponse(**res.json()['Post'])
    
    assert res.status_code == 200
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title
    assert post.created_at == test_posts[0].created_at
    

@pytest.mark.parametrize("title, content, published", [
    ('A New Title', 'Some new content.', True),
    ('Why Is It 90 Degrees During Winter?', 'Seriously, though..', False),
    ('I Like Turtles', '...turtles?', True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post('/posts/', json={
        'title': title, 'content': content, 'published': published})
    
    post_schema = PostResponse(**res.json())
    
    assert res.status_code == 201
    assert post_schema.title == title
    assert post_schema.username == test_user['username']
    assert post_schema.content == content
    assert post_schema.published == published


def test_create_post_with_default_published_value(authorized_client, test_user):
    res = authorized_client.post('/posts/', json={
        'title': 'Some New Title', 'content': 'New content and stuff.'})
    
    post_schema = PostResponse(**res.json())
    
    assert res.status_code == 201
    assert post_schema.title == 'Some New Title'
    assert post_schema.username == test_user['username']
    assert post_schema.content == 'New content and stuff.'
    assert post_schema.published == True


def test_unauthenticated_user_create_post(client):
    res = client.post('/posts/', json={
        'title': 'Some New Title', 'content': 'New content and stuff.'})
    
    assert res.status_code == 401
    

def test_delete_post_authenticated(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204
    
    res = authorized_client.get('/posts/')
    assert len(res.json()) == 3
    
    
def test_delete_post_unauthenticated(client, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_delete_post_that_does_not_exist(authorized_client):
    res = authorized_client.delete('/posts/999')
    assert res.status_code == 404

    
def test_delete_post_unauthorized(authorized_client, test_posts):
    '''Attempts to delete a user's post when the logged in user is not the owner'''
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403
    

def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json={
      'title': 'New Title', 'content': 'New Content', 'published': False   
    })
    
    assert res.status_code == 200
    post = PostResponse(**res.json())

    assert post.title == 'New Title'
    assert post.content == 'New Content'
    assert post.published == False
    
    
def test_update_post_unauthenticated_user(client, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}', json={
      'title': 'New Title', 'content': 'New Content', 'published': False   
    })
    
    assert res.status_code == 401
   
    
def test_update_post_unauthorized_user(authorized_client, test_posts):
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json={
        'title': 'New Title', 'content': 'New Content', 'published': False
    })
    
    assert res.status_code == 403
    

def test_update_post_does_not_exist(authorized_client):
    res = authorized_client.put('/posts/999', json={
        'title': 'New Title', 'content': 'New Content', 'published': False
    })
    
    assert res.status_code == 404
