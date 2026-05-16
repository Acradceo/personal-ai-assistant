import pytest
from backend.app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # We need to set a mock API key for the tests since it relies on os.environ
    # However, the app imports API_KEY at module level. Let's patch it in the tests.
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear tasks before each test
    tasks.clear()
    yield
    # Clear tasks after each test
    tasks.clear()

def test_manage_tasks_unauthorized(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    response = client.get('/api/tasks')
    assert response.status_code == 401

    response = client.post('/api/tasks', json={"title": "Test Task"})
    assert response.status_code == 401

def test_manage_tasks_authorized(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    headers = {"X-API-Key": "test_secret_key"}

    # Test POST (create task)
    response = client.post('/api/tasks', json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Task"

    # Test GET (list tasks)
    response = client.get('/api/tasks', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Test Task"

def test_task_detail_unauthorized(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    # Setup mock task
    tasks[1] = {"id": 1, "title": "Test Task", "status": "pending"}

    response = client.get('/api/tasks/1')
    assert response.status_code == 401

    response = client.put('/api/tasks/1', json={"status": "completed"})
    assert response.status_code == 401

    response = client.delete('/api/tasks/1')
    assert response.status_code == 401

def test_task_detail_authorized(client, mocker):
    mocker.patch('backend.app.API_KEY', 'test_secret_key')
    headers = {"X-API-Key": "test_secret_key"}

    # Setup mock task
    tasks[1] = {"id": 1, "title": "Test Task", "status": "pending"}

    # Test GET
    response = client.get('/api/tasks/1', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Task"

    # Test PUT
    response = client.put('/api/tasks/1', json={"status": "completed"}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "completed"

    # Test DELETE
    response = client.delete('/api/tasks/1', headers=headers)
    assert response.status_code == 200

    # Verify deletion
    assert 1 not in tasks
