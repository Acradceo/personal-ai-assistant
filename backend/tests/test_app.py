import pytest
import json
from backend.app import app, conversation_history, tasks, notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear state before each test
        client.post('/api/clear')
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'ollama_available' in data

def test_get_notes(client):
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'notes' in data
    assert len(data['notes']) == 0

def test_create_note(client):
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': 'This is a test note',
        'tags': ['test']
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Note'
    assert data['content'] == 'This is a test note'
    assert data['tags'] == ['test']
    assert 'id' in data

def test_update_note(client):
    # Create note first
    post_res = client.post('/api/notes', json={
        'title': 'Original Title',
        'content': 'Original content'
    })
    note_id = json.loads(post_res.data)['id']

    # Update it
    response = client.put(f'/api/notes/{note_id}', json={
        'title': 'Updated Title',
        'content': 'Updated content'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Title'
    assert data['content'] == 'Updated content'

def test_delete_note(client):
    # Create note first
    post_res = client.post('/api/notes', json={
        'title': 'To be deleted',
    })
    note_id = json.loads(post_res.data)['id']

    # Delete it
    response = client.delete(f'/api/notes/{note_id}')
    assert response.status_code == 200

    # Verify it's gone
    get_res = client.get('/api/notes')
    data = json.loads(get_res.data)
    assert len(data['notes']) == 0

def test_update_missing_note(client):
    response = client.put('/api/notes/999', json={'title': 'Missing'})
    assert response.status_code == 404

def test_get_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'tasks' in data
    assert len(data['tasks']) == 0

def test_create_task(client):
    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is a test task'
    assert data['status'] == 'pending'
    assert 'id' in data

def test_update_task(client):
    # Create task first
    post_res = client.post('/api/tasks', json={
        'title': 'Original Task Title',
        'description': 'Original description'
    })
    task_id = json.loads(post_res.data)['id']

    # Update it
    response = client.put(f'/api/tasks/{task_id}', json={
        'title': 'Updated Task Title',
        'status': 'completed'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Task Title'
    assert data['status'] == 'completed'

def test_delete_task(client):
    # Create task first
    post_res = client.post('/api/tasks', json={
        'title': 'To be deleted task',
    })
    task_id = json.loads(post_res.data)['id']

    # Delete it
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200

    # Verify it's gone
    get_res = client.get('/api/tasks')
    data = json.loads(get_res.data)
    assert len(data['tasks']) == 0

def test_update_missing_task(client):
    response = client.put('/api/tasks/999', json={'title': 'Missing Task'})
    assert response.status_code == 404

def test_chat_empty_message(client):
    response = client.post('/api/chat', json={'message': ''})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_history(client):
    response = client.get('/api/history')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'history' in data
    assert 'total' in data

def test_clear_data(client):
    # Add some data
    client.post('/api/tasks', json={'title': 'Task 1'})
    client.post('/api/notes', json={'title': 'Note 1'})

    # Clear data
    response = client.post('/api/clear')
    assert response.status_code == 200

    # Verify tasks and notes are empty
    tasks_res = json.loads(client.get('/api/tasks').data)
    assert len(tasks_res['tasks']) == 0

    notes_res = json.loads(client.get('/api/notes').data)
    assert len(notes_res['notes']) == 0
