
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(f'/votes/', json={'post_id': test_posts[3].id, 'direction': 1})
    
    assert res.status_code == 201 
    
    
def test_vote_on_post_twice(authorized_client, test_posts, test_votes):
    res = authorized_client.post(f'/votes/', json={'post_id': test_posts[0].id, 'direction': 1})

    assert res.status_code == 409
    

def test_vote_on_post_unauthenticated(client, test_posts):
    res = client.post('/votes/', json={'post_id': test_posts[0].id, 'direction': 1})
    assert res.status_code == 401


def test_vote_on_post_that_does_not_exist(authorized_client):
    res = authorized_client.post('/votes/', json={'post_id': 999, 'direction': 1})
    
    assert res.status_code == 404


def test_delete_vote(authorized_client, test_votes):
    res = authorized_client.post('/votes/',json={'post_id': test_votes[0].post_id, 'direction': 0})
        
    assert res.status_code == 204


def test_delete_vote_unauthenticated(client, test_votes):
    res = client.post('/votes/',json={'post_id': test_votes[0].post_id, 'direction': 0})
    
    assert res.status_code == 401
    

def test_delete_vote_that_does_not_exist(authorized_client):
    res = authorized_client.post('/votes/', json={'post_id': 999, 'direction': 0})
    
    assert res.status_code == 404
    