import pytest
from backend.app import app, tasks, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    tasks.clear()
    notes.clear()
    yield
    tasks.clear()
    notes.clear()

def test_tasks_pagination(client):
    for i in range(5):
        tasks[i+1] = {"id": i+1, "title": f"Task {i+1}", "status": "pending"}

    # Test without pagination
    res = client.get('/api/tasks')
    assert len(res.get_json()["tasks"]) == 5

    # Test with pagination
    res = client.get('/api/tasks?limit=2&offset=1')
    data = res.get_json()
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["id"] == 2
    assert data["tasks"][1]["id"] == 3
    assert data["total"] == 5
    assert data["limit"] == 2
    assert data["offset"] == 1

def test_notes_pagination(client):
    for i in range(5):
        notes[i+1] = {"id": i+1, "title": f"Note {i+1}", "content": "test"}

    res = client.get('/api/notes?limit=3&offset=2')
    data = res.get_json()
    assert len(data["notes"]) == 3
    assert data["notes"][0]["id"] == 3
    assert data["notes"][2]["id"] == 5
    assert data["total"] == 5
