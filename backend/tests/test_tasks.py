import pytest
from backend.app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear tasks history before each test
    tasks.clear()
    yield
    # Clear tasks history after each test
    tasks.clear()

def test_task_detail_get_happy_path(client):
    tasks[1] = {"id": 1, "title": "Test Task", "description": "Desc", "status": "pending"}
    response = client.get('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Task"

def test_task_detail_get_not_found(client):
    response = client.get('/api/tasks/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Task not found"

def test_task_detail_put_happy_path(client):
    tasks[1] = {"id": 1, "title": "Old Task", "description": "Old Desc", "status": "pending"}
    response = client.put('/api/tasks/1', json={"title": "New Task", "status": "completed"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "New Task"
    assert data["status"] == "completed"
    assert data["description"] == "Old Desc"
    assert tasks[1]["title"] == "New Task"

def test_task_detail_put_invalid_json(client):
    tasks[1] = {"id": 1, "title": "Old Task", "description": "Old Desc", "status": "pending"}
    response = client.put('/api/tasks/1', data="invalid json", content_type='application/json')
    # It hits the global exception handler because request.get_json() fails with BadRequest when sending invalid json.
    # Flask translates it to a 500 when it hits the generic try/except block.
    assert response.status_code == 500

def test_task_detail_put_empty_json(client):
    tasks[1] = {"id": 1, "title": "Old Task", "description": "Old Desc", "status": "pending"}
    response = client.put('/api/tasks/1', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid JSON"

def test_task_detail_put_not_found(client):
    response = client.put('/api/tasks/999', json={"title": "New Task"})
    assert response.status_code == 404

def test_task_detail_delete_happy_path(client):
    tasks[1] = {"id": 1, "title": "Task to Delete"}
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Task deleted"
    assert data["task"]["title"] == "Task to Delete"
    assert 1 not in tasks

def test_task_detail_delete_not_found(client):
    response = client.delete('/api/tasks/999')
    assert response.status_code == 404
