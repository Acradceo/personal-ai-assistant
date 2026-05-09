import os
os.environ['API_KEY'] = 'test_secret_key'

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_clear_no_auth(client):
    response = client.post('/api/clear')
    assert response.status_code == 401

def test_clear_with_auth(client):
    response = client.post('/api/clear', headers={'X-API-Key': 'test_secret_key'})
    assert response.status_code == 200

def test_clear_with_bearer_auth(client):
    response = client.post('/api/clear', headers={'Authorization': 'Bearer test_secret_key'})
    assert response.status_code == 200

def test_clear_wrong_auth(client):
    response = client.post('/api/clear', headers={'X-API-Key': 'wrong'})
    assert response.status_code == 401
