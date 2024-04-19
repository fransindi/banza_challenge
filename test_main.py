from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_client():
    response = client.post('/client/', json={'name': 'fran'})
    response2 = client.post('/client/', json={'name': ''})
    response3 = client.post('/client/', json={'name': 'aghata'})
    assert response.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 200




def test_get_all_clients():
    response = client.get("/client/all")
    assert response.status_code == 200
    
def test_get_client():
    client_id = 2
    response = client.get(f'/client/{client_id}')
    response_2 = client.get(f'/client/0')
    assert response.status_code == 200
    assert response_2.status_code == 404

def test_delete_client():
    client_id = 7
    response = client.delete(f'/client/{client_id}')
    response2 = client.delete(f'/client/0')
    assert response.status_code == 200
    assert response2.status_code == 404

def test_post_cat_cli():
    response = client.post('/client/cat_cli',
                           json={
                               'client_id': '0',
                               'category_id': '0'
                           })
    response2 = client.post('/client/cat_cli',
                           json={
                               'client_id': '1',
                               'category_id': '0'
                           })
    response3 = client.post('/client/cat_cli',
                           json={
                               'client_id': '0',
                               'category_id': '1'
                           })
    response4 = client.post('/client/cat_cli',
                           json={
                               'client_id': '1',
                               'category_id': '1'
                           })
    response5 = client.post('/client/cat_cli',
                           json={
                               'client_id': '5',
                               'category_id': '2'
                           })
    assert response.status_code == 400
    assert response2.status_code == 400
    assert response3.status_code == 400
    assert response4.status_code == 400
    assert response5.status_code == 200
    

# TEST DB_MOVEMENT

def test_post_movement():
    response = client.post('/movement/',
                          json={
                              'account_id': '4',
                              'transaction_type': 'gasto',
                              'amount': '2500'
                          })
    response2 = client.post('/movement/',
                          json={
                              'account_id': '0',
                              'transaction_type': 'ingreso',
                              'amount': '2500'
                          })
    response3 = client.post('/movement/',
                          json={
                              'account_id': '4',
                              'transaction_type': 'ingreso',
                              'amount': '-2500'
                          })
    response4 = client.post('/movement/',
                          json={
                              'account_id': '4',
                              'transaction_type': 'ingreso',
                              'amount': '2500'
                          })

    assert response.status_code == 400
    assert response2.status_code == 404
    assert response3.status_code == 400
    assert response4.status_code == 200

def test_delete_movement():
    response = client.delete('/movement/0')
    response2 = client.delete('/movement/11')
    assert response.status_code == 404
    assert response2.status_code == 200

def test_get_movement():
    response = client.get('/movement/0')
    response2 = client.get('/movement/5')
    assert response.status_code == 404
    assert response2.status_code == 200

def test_get_dolar_price():
    response = client.get('/movement/get_dolar_bolsa/')
    assert response.status_code == 200


def test_get_total_usd():
    response = client.get('/movement/total_usd/0')
    response2 = client.get('/movement/total_usd/4')

    assert response.status_code == 404
    assert response2.status_code == 200