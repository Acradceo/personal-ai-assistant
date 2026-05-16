import pytest
from backend import app as app_module
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup some dummy data
    app_module.conversation_history.extend([{"role": "user", "content": "hi"}])
    app_module.tasks[1] = {"id": 1, "title": "Test Task", "status": "pending"}
    app_module.notes[1] = {"id": 1, "title": "Test Note", "content": "Test"}
    app_module.next_task_id = 2
    app_module.next_note_id = 2

    # Save the original API_KEY
    original_api_key = app_module.API_KEY
    app_module.API_KEY = "test_secret_key"

    yield

    # Teardown: clear everything back to defaults
    app_module.conversation_history.clear()
    app_module.tasks.clear()
    app_module.notes.clear()
    app_module.next_task_id = 1
    app_module.next_note_id = 1
    app_module.API_KEY = original_api_key

def test_clear_data_success(client):
    headers = {"X-API-Key": "test_secret_key"}
    response = client.post('/api/clear', headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "All data cleared"

    # Verify state is reset
    assert len(app_module.conversation_history) == 0
    assert len(app_module.tasks) == 0
    assert len(app_module.notes) == 0
    assert app_module.next_task_id == 1
    assert app_module.next_note_id == 1

def test_clear_data_unauthorized_no_key(client):
    response = client.post('/api/clear')

    assert response.status_code == 401

    # Verify state is NOT reset
    assert len(app_module.conversation_history) == 1
    assert len(app_module.tasks) == 1
    assert len(app_module.notes) == 1

def test_clear_data_unauthorized_wrong_key(client):
    headers = {"X-API-Key": "wrong_key"}
    response = client.post('/api/clear', headers=headers)

    assert response.status_code == 401

    # Verify state is NOT reset
    assert len(app_module.conversation_history) == 1
    assert len(app_module.tasks) == 1

def test_clear_data_server_not_configured(client):
    app_module.API_KEY = None
    headers = {"X-API-Key": "test_secret_key"}
    response = client.post('/api/clear', headers=headers)

    assert response.status_code == 500

    # Verify state is NOT reset
    assert len(app_module.tasks) == 1

def test_clear_data_internal_error(client, mocker):
    headers = {"X-API-Key": "test_secret_key"}

    mocker.patch('backend.app.logger.warning', side_effect=Exception('Test Error'))

    response = client.post('/api/clear', headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Test Error"
