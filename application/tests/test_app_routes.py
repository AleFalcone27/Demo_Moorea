# Integration test 

def test_root(client):
    response = client.get('/')
    assert response.status_code == 302
    


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    
    

def test_logout(client):
    client.get("/logout")
    with client.session_transaction() as session:
        assert 'user_name' not in session