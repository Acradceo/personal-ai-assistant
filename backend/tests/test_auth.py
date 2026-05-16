import pytest
from flask import jsonify
from backend.app import app

@pytest.fixture
def client():
    # Use the existing Flask app and configure it for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_require_api_key_unconfigured(client, mocker):
    mocker.patch('backend.app.API_KEY', None)
    response = client.post('/api/clear')
    assert response.status_code == 500
    assert response.get_json() == {"error": "API_KEY not configured on server"}

def test_require_api_key_no_token(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    response = client.post('/api/clear')
    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}

def test_require_api_key_invalid_token(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')

    # Test invalid Bearer token
    response = client.post('/api/clear', headers={"Authorization": "Bearer wrong_key"})
    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized"}

    # Test invalid X-API-Key
    response = client.post('/api/clear', headers={"X-API-Key": "wrong_key"})
    assert response.status_code == 401

def test_require_api_key_valid_bearer_token(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    response = client.post('/api/clear', headers={"Authorization": "Bearer test_secret_key"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "All data cleared"}

def test_require_api_key_valid_x_api_key(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    response = client.post('/api/clear', headers={"X-API-Key": "test_secret_key"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "All data cleared"}
