import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        client.post('/api/clear')
        yield client
        client.post('/api/clear')

def test_update_task_success(client):
    # First, create a task
    create_response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    assert create_response.status_code == 201
    task_id = create_response.get_json()['id']

    # Now, update the task
    update_response = client.put(f'/api/tasks/{task_id}', json={
        'title': 'Updated Task',
        'status': 'completed'
    })
    assert update_response.status_code == 200
    updated_task = update_response.get_json()
    assert updated_task['title'] == 'Updated Task'
    assert updated_task['status'] == 'completed'
    assert updated_task['id'] == task_id

def test_delete_task_success(client):
    # First, create a task
    create_response = client.post('/api/tasks', json={
        'title': 'Test Task to Delete'
    })
    assert create_response.status_code == 201
    task_id = create_response.get_json()['id']

    # Now, delete the task
    delete_response = client.delete(f'/api/tasks/{task_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json() == {"message": "Task deleted"}

    # Verify it's deleted by trying to update it
    update_response = client.put(f'/api/tasks/{task_id}', json={'title': 'test'})
    assert update_response.status_code == 404

def test_update_task_not_found(client):
    # Try to update a non-existent task
    update_response = client.put('/api/tasks/999', json={'title': 'test'})
    assert update_response.status_code == 404
    assert update_response.get_json() == {"error": "Task not found"}

def test_delete_task_not_found(client):
    # Try to delete a non-existent task
    delete_response = client.delete('/api/tasks/999')
    assert delete_response.status_code == 404
    assert delete_response.get_json() == {"error": "Task not found"}
