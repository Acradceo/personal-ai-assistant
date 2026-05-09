import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config.update({
        "TESTING": True,
    })

    with flask_app.test_client() as client:
        # Reset the data before each test
        client.post('/api/clear')
        yield client

def test_get_notes_empty(client):
    """Test getting notes when the list is empty."""
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert "notes" in data
    assert data["notes"] == []

def test_create_note(client):
    """Test creating a new note."""
    new_note = {
        "title": "Test Note",
        "content": "This is a test note.",
        "tags": ["test", "pytest"]
    }
    response = client.post('/api/notes', json=new_note)
    assert response.status_code == 201
    data = response.get_json()

    assert data["id"] == 1
    assert data["title"] == new_note["title"]
    assert data["content"] == new_note["content"]
    assert "created_at" in data
    assert data["tags"] == new_note["tags"]

def test_get_notes_populated(client):
    """Test getting notes after adding one."""
    # Add a note
    new_note = {
        "title": "Another Note",
        "content": "More content."
    }
    client.post('/api/notes', json=new_note)

    # Retrieve notes
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()

    assert len(data["notes"]) == 1
    assert data["notes"][0]["title"] == "Another Note"
    assert data["notes"][0]["content"] == "More content."
    # Tags default to an empty list
    assert data["notes"][0]["tags"] == []

def test_update_note(client):
    """Test updating an existing note."""
    # Create note
    client.post('/api/notes', json={"title": "Old Title", "content": "Old Content"})

    # Update note
    update_data = {"title": "New Title", "content": "New Content", "tags": ["updated"]}
    response = client.put('/api/notes/1', json=update_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"
    assert data["tags"] == ["updated"]

def test_update_note_not_found(client):
    """Test updating a non-existent note."""
    response = client.put('/api/notes/999', json={"title": "Should Fail"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"

def test_delete_note(client):
    """Test deleting an existing note."""
    # Create note
    client.post('/api/notes', json={"title": "To be deleted", "content": "Delete me"})

    # Verify it exists
    assert len(client.get('/api/notes').get_json()["notes"]) == 1

    # Delete note
    response = client.delete('/api/notes/1')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Note deleted"

    # Verify it's gone
    assert len(client.get('/api/notes').get_json()["notes"]) == 0

def test_delete_note_not_found(client):
    """Test deleting a non-existent note."""
    response = client.delete('/api/notes/999')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"
