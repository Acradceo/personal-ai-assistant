from backend.app import app, tasks, notes
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_tasks_pagination(client):
    tasks.clear()
    for i in range(10):
        tasks[i+1] = {"id": i+1, "title": f"Task {i+1}"}

    # Test valid pagination
    resp = client.get('/api/tasks?limit=3&offset=2')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['tasks']) == 3
    assert data['tasks'][0]['id'] == 3

    # Test backward compatibility
    resp = client.get('/api/tasks')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['tasks']) == 10

    # Test invalid limit
    resp = client.get('/api/tasks?limit=-1')
    assert resp.status_code == 400
    assert "non-negative" in resp.get_json()['error']

    # Test bad value
    resp = client.get('/api/tasks?limit=abc')
    assert resp.status_code == 400
    assert "valid integers" in resp.get_json()['error']

def test_notes_pagination(client):
    notes.clear()
    for i in range(10):
        notes[i+1] = {"id": i+1, "title": f"Note {i+1}"}

    # Test valid pagination
    resp = client.get('/api/notes?limit=4&offset=5')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['notes']) == 4
    assert data['notes'][0]['id'] == 6

    # Test backward compatibility
    resp = client.get('/api/notes')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data['notes']) == 10

    # Test invalid offset
    resp = client.get('/api/notes?offset=-5')
    assert resp.status_code == 400
    assert "non-negative" in resp.get_json()['error']
