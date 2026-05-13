import pytest
from backend.app import app
import backend.app as backend_app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_stats_auth_missing_api_key_server_config(client, mocker):
    mocker.patch.object(backend_app, 'API_KEY', None)
    response = client.get('/api/stats')
    assert response.status_code == 500
    assert response.get_json()['error'] == "API_KEY not configured on server"

def test_stats_auth_unauthorized(client, mocker):
    mocker.patch.object(backend_app, 'API_KEY', 'secret_test_key')
    response = client.get('/api/stats')
    assert response.status_code == 401
    assert response.get_json()['error'] == "Unauthorized"

def test_stats_auth_wrong_key(client, mocker):
    mocker.patch.object(backend_app, 'API_KEY', 'secret_test_key')
    response = client.get('/api/stats', headers={'X-API-Key': 'wrong_key'})
    assert response.status_code == 401
    assert response.get_json()['error'] == "Unauthorized"

def test_stats_auth_success_x_api_key(client, mocker):
    mocker.patch.object(backend_app, 'API_KEY', 'secret_test_key')
    response = client.get('/api/stats', headers={'X-API-Key': 'secret_test_key'})
    assert response.status_code == 200
    assert 'tasks_count' in response.get_json()

def test_stats_auth_success_bearer(client, mocker):
    mocker.patch.object(backend_app, 'API_KEY', 'secret_test_key')
    response = client.get('/api/stats', headers={'Authorization': 'Bearer secret_test_key'})
    assert response.status_code == 200
    assert 'tasks_count' in response.get_json()
