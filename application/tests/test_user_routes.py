# Integration test 

def test_user(client):
    response = client.get("/user")
    assert response.status_code == 302



def test_user_session(client):
    response = client.get("/user")
    with client.session_transaction() as session:
        assert session == {'_flashes': [('message', 'Ingresa tus credenciales para iniciar cesion primero')]}



def test_user_done(client):
    response = client.get("/user/done")
    assert response.status_code == 308 
    



