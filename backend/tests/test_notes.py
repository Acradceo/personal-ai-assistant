import pytest
import json
from backend.app import app, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear notes dictionary before each test
    notes.clear()

    # We also need to reset the next_note_id in the module, but since it's a global variable,
    # the cleanest way without importing and changing the global in app.py directly for every test
    # is to rely on standard dictionary behavior, but let's actually try to import and reset it
    import backend.app
    backend.app.next_note_id = 1

    yield
    # Clear notes dictionary after each test
    notes.clear()

def test_create_note_success(client):
    response = client.post('/api/notes', json={"title": "Test Note", "content": "This is a test note.", "tags": ["test"]})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note."
    assert "test" in data["tags"]
    assert "id" in data
    assert len(notes) == 1

def test_create_note_missing_title(client):
    response = client.post('/api/notes', json={"content": "Missing title"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing required field: title"
    assert len(notes) == 0

def test_get_all_notes_empty(client):
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert data["notes"] == []

def test_get_all_notes_with_data(client):
    client.post('/api/notes', json={"title": "Note 1"})
    client.post('/api/notes', json={"title": "Note 2"})

    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["notes"]) == 2
    assert data["notes"][0]["title"] == "Note 1"
    assert data["notes"][1]["title"] == "Note 2"

def test_get_single_note_success(client):
    create_resp = client.post('/api/notes', json={"title": "Single Note"})
    note_id = create_resp.get_json()["id"]

    response = client.get(f'/api/notes/{note_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Single Note"
    assert data["id"] == note_id

def test_get_single_note_not_found(client):
    response = client.get('/api/notes/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Note not found"

def test_update_note_success(client):
    create_resp = client.post('/api/notes', json={"title": "Old Title", "content": "Old Content"})
    note_id = create_resp.get_json()["id"]

    response = client.put(f'/api/notes/{note_id}', json={
        "title": "New Title",
        "content": "New Content",
        "tags": ["updated"]
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"
    assert "updated" in data["tags"]

    # Verify it was updated in the notes dict
    assert notes[note_id]["title"] == "New Title"

def test_update_note_invalid_json(client):
    create_resp = client.post('/api/notes', json={"title": "Old Title"})
    note_id = create_resp.get_json()["id"]

    # In Flask, request.get_json() raises 400 Bad Request by default when parsing fails.
    # To bypass automatic 400 response from Flask and hit our code's `if not data` we can pass valid empty JSON.
    # An empty dictionary {} evaluates to False in Python, triggering the 400 Invalid JSON response.
    response = client.put(f'/api/notes/{note_id}', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid JSON"

def test_update_note_not_found(client):
    response = client.put('/api/notes/999', json={"title": "New Title"})
    assert response.status_code == 404

def test_delete_note_success(client):
    create_resp = client.post('/api/notes', json={"title": "To Delete"})
    note_id = create_resp.get_json()["id"]

    assert len(notes) == 1

    response = client.delete(f'/api/notes/{note_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Note deleted"
    assert data["note"]["title"] == "To Delete"

    assert len(notes) == 0

def test_delete_note_not_found(client):
    response = client.delete('/api/notes/999')
    assert response.status_code == 404
