import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear data before each test directly
        from app import tasks
        tasks.clear()
        yield client

def test_get_tasks_empty(client):
    """Test getting tasks when list is empty"""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert len(data["tasks"]) == 0

def test_create_task(client):
    """Test creating a new task"""
    new_task = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    response = client.post('/api/tasks', json=new_task)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == "pending"
    assert "created_at" in data

def test_get_tasks_after_create(client):
    """Test getting tasks after creating one"""
    # Create a task first
    new_task = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    client.post('/api/tasks', json=new_task)

    # Get tasks
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert len(data["tasks"]) == 1

    task = data["tasks"][0]
    assert task["title"] == "Test Task"
    assert task["description"] == "This is a test task"
    assert task["status"] == "pending"
