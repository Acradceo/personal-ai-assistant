import pytest
from backend.app import app, tasks, notes, next_task_id, next_note_id

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear state
    import backend.app as app_module
    app_module.tasks.clear()
    app_module.notes.clear()
    app_module.next_task_id = 1
    app_module.next_note_id = 1

    # Populate tasks
    for i in range(1, 6):
        app_module.tasks[i] = {"id": i, "title": f"Task {i}"}
    app_module.next_task_id = 6

    # Populate notes
    for i in range(1, 6):
        app_module.notes[i] = {"id": i, "title": f"Note {i}"}
    app_module.next_note_id = 6

    yield

    app_module.tasks.clear()
    app_module.notes.clear()


def test_tasks_pagination(client):
    # Test limit only
    response = client.get('/api/tasks?limit=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 2
    assert data['total'] == 5
    assert data['tasks'][0]['id'] == 1
    assert data['tasks'][1]['id'] == 2

    # Test limit and offset
    response = client.get('/api/tasks?limit=2&offset=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 2
    assert data['total'] == 5
    assert data['tasks'][0]['id'] == 3
    assert data['tasks'][1]['id'] == 4

    # Test backward compatibility (no params)
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 5
    assert data['total'] == 5

def test_notes_pagination(client):
    # Test limit only
    response = client.get('/api/notes?limit=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['notes']) == 2
    assert data['total'] == 5
    assert data['notes'][0]['id'] == 1
    assert data['notes'][1]['id'] == 2

    # Test limit and offset
    response = client.get('/api/notes?limit=2&offset=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['notes']) == 2
    assert data['total'] == 5
    assert data['notes'][0]['id'] == 3
    assert data['notes'][1]['id'] == 4

    # Test backward compatibility (no params)
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['notes']) == 5
    assert data['total'] == 5

def test_pagination_invalid_params(client):
    response = client.get('/api/tasks?limit=abc')
    assert response.status_code == 400

    response = client.get('/api/notes?offset=xyz')
    assert response.status_code == 400

def test_pagination_negative_params(client):
    response = client.get('/api/tasks?limit=-1')
    assert response.status_code == 400

    response = client.get('/api/notes?offset=-5')
    assert response.status_code == 400
