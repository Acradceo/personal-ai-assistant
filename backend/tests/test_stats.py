import pytest
import os
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_stats_unauthorized(client):
    response = client.get('/api/stats')
    assert response.status_code in [401, 500]  # Either Unauthorized or API_KEY not configured

def test_stats_authorized(client, monkeypatch):
    # Setup test API key
    test_key = "test_api_key_123"
    monkeypatch.setattr('backend.app.API_KEY', test_key)

    headers = {
        'X-API-Key': test_key
    }
    response = client.get('/api/stats', headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert 'tasks_count' in data
    assert 'notes_count' in data
    assert 'history_length' in data
