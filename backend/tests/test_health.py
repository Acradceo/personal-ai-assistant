import pytest
from backend.app import app
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check_happy_path(client):
    response = client.get('/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

    # Check if timestamp is a valid ISO format string
    try:
        datetime.fromisoformat(data['timestamp'])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

    assert isinstance(data['ollama_available'], bool)

def test_health_check_ollama_available(client, mocker):
    # Mock llm to be not None
    mocker.patch('backend.app.llm', mocker.MagicMock())

    response = client.get('/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['ollama_available'] is True

def test_health_check_ollama_unavailable(client, mocker):
    # Mock llm to be None
    mocker.patch('backend.app.llm', None)

    response = client.get('/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['ollama_available'] is False
