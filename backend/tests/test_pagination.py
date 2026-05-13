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

    # Populate with some dummy data
    for i in range(1, 11):
        tasks[i] = {'id': i, 'title': f'Task {i}'}
        notes[i] = {'id': i, 'title': f'Note {i}'}

    yield

    # Clear tasks and notes after each test
    tasks.clear()
    notes.clear()

def test_tasks_pagination_default(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 10
    assert data['total'] == 10

def test_tasks_pagination_limit(client):
    response = client.get('/api/tasks?limit=5')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 5
    assert data['tasks'][0]['id'] == 1
    assert data['tasks'][4]['id'] == 5
    assert data['total'] == 10

def test_tasks_pagination_offset(client):
    response = client.get('/api/tasks?offset=5')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 5
    assert data['tasks'][0]['id'] == 6
    assert data['tasks'][4]['id'] == 10
    assert data['total'] == 10

def test_tasks_pagination_limit_and_offset(client):
    response = client.get('/api/tasks?limit=3&offset=4')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 3
    assert data['tasks'][0]['id'] == 5
    assert data['tasks'][1]['id'] == 6
    assert data['tasks'][2]['id'] == 7
    assert data['total'] == 10

def test_tasks_pagination_invalid_params(client):
    response = client.get('/api/tasks?limit=-5&offset=-2')
    assert response.status_code == 200
    data = response.get_json()
    # It should fallback to default limit None (all results) and offset 0
    assert len(data['tasks']) == 10
    assert data['total'] == 10

def test_notes_pagination_limit_and_offset(client):
    response = client.get('/api/notes?limit=4&offset=2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['notes']) == 4
    assert data['notes'][0]['id'] == 3
    assert data['notes'][3]['id'] == 6
    assert data['total'] == 10
