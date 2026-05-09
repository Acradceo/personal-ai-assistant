import pytest
from backend.app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_update_non_existent_task(client):
    # Setup
    tasks.clear() # Ensure no tasks exist

    # PUT to non-existent ID
    response = client.put('/api/tasks/999', json={'title': 'New Title'})

    # Assertions
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}

def test_delete_non_existent_task(client):
    # Setup
    tasks.clear() # Ensure no tasks exist

    # DELETE to non-existent ID
    response = client.delete('/api/tasks/999')

    # Assertions
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}
