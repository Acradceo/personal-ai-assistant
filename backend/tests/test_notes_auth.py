import pytest
from backend.app import app, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # We need to set a dummy API key for testing
    import backend.app as app_module
    app_module.API_KEY = "test_secret_key"

    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    notes.clear()
    import backend.app as app_module
    app_module.next_note_id = 1
    yield
    notes.clear()
    app_module.next_note_id = 1

def test_notes_endpoints_require_auth(client):
    # Test GET /api/notes without auth
    response = client.get('/api/notes')
    assert response.status_code == 401

    # Test POST /api/notes without auth
    response = client.post('/api/notes', json={"title": "Test Note"})
    assert response.status_code == 401

    # Add a dummy note directly to test specific note endpoints
    notes[1] = {"id": 1, "title": "Dummy", "content": "Dummy content", "tags": []}

    # Test GET /api/notes/<id> without auth
    response = client.get('/api/notes/1')
    assert response.status_code == 401

    # Test PUT /api/notes/<id> without auth
    response = client.put('/api/notes/1', json={"title": "Updated Dummy"})
    assert response.status_code == 401

    # Test DELETE /api/notes/<id> without auth
    response = client.delete('/api/notes/1')
    assert response.status_code == 401

def test_notes_endpoints_with_auth(client):
    headers = {"Authorization": "Bearer test_secret_key"}

    # Test POST /api/notes with auth
    response = client.post('/api/notes', headers=headers, json={"title": "My Note", "content": "Secret"})
    assert response.status_code == 201
    note_id = response.get_json()["id"]

    # Test GET /api/notes with auth
    response = client.get('/api/notes', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()["notes"]) == 1

    # Test GET /api/notes/<id> with auth
    response = client.get(f'/api/notes/{note_id}', headers=headers)
    assert response.status_code == 200

    # Test PUT /api/notes/<id> with auth
    response = client.put(f'/api/notes/{note_id}', headers=headers, json={"title": "Updated Note"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "Updated Note"

    # Test DELETE /api/notes/<id> with auth
    response = client.delete(f'/api/notes/{note_id}', headers=headers)
    assert response.status_code == 200

    # Confirm deletion
    response = client.get('/api/notes', headers=headers)
    assert len(response.get_json()["notes"]) == 0
