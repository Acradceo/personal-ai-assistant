import pytest
from backend.app import app
import os
import secrets

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_stats_missing_api_key_on_server(client, mocker):
    # If API_KEY is missing on the server, it should return 500
    mocker.patch('backend.app.API_KEY', None)
    response = client.get('/api/stats')
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "API_KEY not configured on server"

def test_stats_missing_auth(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_key_123')
    response = client.get('/api/stats')
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Unauthorized"

def test_stats_invalid_auth_header(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_key_123')
    response = client.get('/api/stats', headers={"Authorization": "Bearer wrong_key"})
    assert response.status_code == 401

def test_stats_invalid_auth_x_api_key(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_key_123')
    response = client.get('/api/stats', headers={"X-API-Key": "wrong_key"})
    assert response.status_code == 401

def test_stats_valid_auth_bearer(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_key_123')
    response = client.get('/api/stats', headers={"Authorization": "Bearer test_key_123"})
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks_count" in data
    assert "notes_count" in data

def test_stats_valid_auth_x_api_key(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_key_123')
    response = client.get('/api/stats', headers={"X-API-Key": "test_key_123"})
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks_count" in data
    assert "notes_count" in data
