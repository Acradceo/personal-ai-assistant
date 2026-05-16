import pytest
from backend.app import app, tasks, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear the global state before each test
    tasks.clear()
    notes.clear()

    # We must reset the global counters through globals() just like the API does
    import backend.app as backend_app
    backend_app.next_task_id = 1
    backend_app.next_note_id = 1

    yield

    tasks.clear()
    notes.clear()
    backend_app.next_task_id = 1
    backend_app.next_note_id = 1

def test_tasks_crud(client):
    # Create task
    response = client.post('/api/tasks', json={"title": "Test Task", "description": "A description"})
    assert response.status_code == 201
    task = response.get_json()
    assert task["id"] == 1
    assert task["title"] == "Test Task"
    assert task["description"] == "A description"
    assert task["status"] == "pending"
    assert "created_at" in task

    # Get all tasks
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["id"] == 1

    # Get single task
    response = client.get('/api/tasks/1')
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test Task"

    # Update task (with whitelist test)
    response = client.put('/api/tasks/1', json={"title": "Updated Task", "status": "completed", "invalid_field": "hacker"})
    assert response.status_code == 200
    task = response.get_json()
    assert task["title"] == "Updated Task"
    assert task["status"] == "completed"
    assert "invalid_field" not in task

    # Delete task
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200

    # Verify deletion
    response = client.get('/api/tasks/1')
    assert response.status_code == 404

def test_notes_crud(client):
    # Create note
    response = client.post('/api/notes', json={"title": "Test Note", "content": "Note content", "tags": ["test"]})
    assert response.status_code == 201
    note = response.get_json()
    assert note["id"] == 1
    assert note["title"] == "Test Note"
    assert note["content"] == "Note content"
    assert note["tags"] == ["test"]
    assert "created_at" in note

    # Get all notes
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["notes"]) == 1
    assert data["notes"][0]["id"] == 1

    # Get single note
    response = client.get('/api/notes/1')
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test Note"

    # Update note
    response = client.put('/api/notes/1', json={"title": "Updated Note", "content": "New content", "invalid_field": "hacker"})
    assert response.status_code == 200
    note = response.get_json()
    assert note["title"] == "Updated Note"
    assert note["content"] == "New content"
    assert "invalid_field" not in note

    # Delete note
    response = client.delete('/api/notes/1')
    assert response.status_code == 200

    # Verify deletion
    response = client.get('/api/notes/1')
    assert response.status_code == 404

def test_missing_title_error(client):
    response = client.post('/api/tasks', json={"description": "No title"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing required field: title"

    response = client.post('/api/notes', json={"content": "No title"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing required field: title"
