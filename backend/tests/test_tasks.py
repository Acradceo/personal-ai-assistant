import pytest
from backend.app import app, tasks
import backend.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear tasks dictionary and reset next_task_id before each test
    tasks.clear()
    backend.app.next_task_id = 1
    yield
    # Clear tasks dictionary and reset next_task_id after each test
    tasks.clear()
    backend.app.next_task_id = 1

def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert len(data["tasks"]) == 0

def test_create_task_success(client):
    response = client.post('/api/tasks', json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    data = response.get_json()

    # Check response
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data

    # Check internal state
    assert len(tasks) == 1
    task_id = data["id"]
    assert task_id in tasks
    assert tasks[task_id]["title"] == "Test Task"

def test_create_task_missing_title(client):
    response = client.post('/api/tasks', json={"description": "Test Description"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing required field: title"
    assert len(tasks) == 0

def test_create_task_invalid_json(client):
    response = client.post('/api/tasks', data="not a json", content_type='application/json')
    # Because request.get_json() raises a BadRequest exception when invalid JSON is provided,
    # the generic exception handler catches it and returns 500, but we test that it responds
    # with an error message and state isn't modified.
    # In a more robust setup, you might want to return 400, but we test the current behavior.
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert len(tasks) == 0

def test_get_multiple_tasks(client):
    # Add tasks
    client.post('/api/tasks', json={"title": "Task 1"})
    client.post('/api/tasks', json={"title": "Task 2"})

    # Get all tasks
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()

    assert "tasks" in data
    assert len(data["tasks"]) == 2

    titles = [task["title"] for task in data["tasks"]]
    assert "Task 1" in titles
    assert "Task 2" in titles
