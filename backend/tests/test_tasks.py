import pytest
from backend.app import app, tasks
import backend.app as backend_app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    backend_app.API_KEY = "test_api_key"
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    tasks.clear()
    backend_app.next_task_id = 1
    yield
    tasks.clear()

def test_task_detail_requires_auth(client):
    tasks[1] = {
        "id": 1,
        "title": "Test Task",
        "description": "Test",
        "status": "pending",
        "created_at": "2023-01-01T00:00:00"
    }

    response = client.get('/api/tasks/1')
    assert response.status_code == 401

    response = client.get('/api/tasks/1', headers={"X-API-Key": "wrong"})
    assert response.status_code == 401

    response = client.get('/api/tasks/1', headers={"X-API-Key": "test_api_key"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test Task"

def test_task_detail_put_requires_auth(client):
    tasks[1] = {
        "id": 1,
        "title": "Test Task",
        "description": "Test",
        "status": "pending",
        "created_at": "2023-01-01T00:00:00"
    }

    response = client.put('/api/tasks/1', json={"status": "completed"})
    assert response.status_code == 401

    response = client.put('/api/tasks/1', json={"status": "completed"}, headers={"X-API-Key": "test_api_key"})
    assert response.status_code == 200
    assert tasks[1]["status"] == "completed"

def test_task_detail_delete_requires_auth(client):
    tasks[1] = {
        "id": 1,
        "title": "Test Task",
        "description": "Test",
        "status": "pending",
        "created_at": "2023-01-01T00:00:00"
    }

    response = client.delete('/api/tasks/1')
    assert response.status_code == 401

    response = client.delete('/api/tasks/1', headers={"X-API-Key": "test_api_key"})
    assert response.status_code == 200
    assert 1 not in tasks
