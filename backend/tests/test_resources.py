import pytest
from backend.app import app, tasks, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear tasks and notes before each test
    tasks.clear()
    notes.clear()
    # Also reset the next IDs if needed, although direct dictionary manipulation in tests might not use them.
    # We will seed the data manually in the tests to test the endpoints.
    yield
    # Clear tasks and notes after each test
    tasks.clear()
    notes.clear()


def test_task_detail_get(client):
    tasks[1] = {"id": 1, "title": "Test Task", "description": "Desc", "status": "pending"}

    response = client.get('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Task"

    response = client.get('/api/tasks/2')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_task_detail_put(client):
    tasks[1] = {"id": 1, "title": "Test Task", "description": "Desc", "status": "pending"}

    response = client.put('/api/tasks/1', json={"title": "Updated Task", "status": "completed"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "completed"
    assert tasks[1]["title"] == "Updated Task"

    # Test invalid JSON
    response = client.put('/api/tasks/1')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid JSON"


def test_task_detail_delete(client):
    tasks[1] = {"id": 1, "title": "Test Task", "description": "Desc", "status": "pending"}

    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted"
    assert 1 not in tasks


def test_note_detail_get(client):
    notes[1] = {"id": 1, "title": "Test Note", "content": "Content", "tags": []}

    response = client.get('/api/notes/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Note"

    response = client.get('/api/notes/2')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"


def test_note_detail_put(client):
    notes[1] = {"id": 1, "title": "Test Note", "content": "Content", "tags": []}

    response = client.put('/api/notes/1', json={"title": "Updated Note", "tags": ["important"]})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Note"
    assert data["tags"] == ["important"]
    assert notes[1]["title"] == "Updated Note"

    # Test invalid JSON
    response = client.put('/api/notes/1')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid JSON"


def test_note_detail_delete(client):
    notes[1] = {"id": 1, "title": "Test Note", "content": "Content", "tags": []}

    response = client.delete('/api/notes/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Note deleted"
    assert 1 not in notes
