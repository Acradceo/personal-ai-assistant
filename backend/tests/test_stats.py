import pytest
import os
from unittest.mock import patch
from backend.app import app, tasks, notes, conversation_history
import backend.app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear state before each test
    tasks.clear()
    notes.clear()
    conversation_history.clear()

    yield

    # Clear state after each test
    tasks.clear()
    notes.clear()
    conversation_history.clear()

def test_get_stats_empty(client):
    response = client.get('/api/stats')
    assert response.status_code == 200

    data = response.get_json()
    assert data["tasks_count"] == 0
    assert data["notes_count"] == 0
    assert data["history_length"] == 0
    assert "next_task_id" in data
    assert "next_note_id" in data
    assert "timestamp" in data

def test_get_stats_with_data(client):
    # Populate data
    tasks[1] = {"id": 1, "title": "Task 1", "description": "Desc 1", "status": "pending"}
    tasks[2] = {"id": 2, "title": "Task 2", "description": "Desc 2", "status": "completed"}

    notes[1] = {"id": 1, "title": "Note 1", "content": "Content 1", "tags": []}

    conversation_history.append({"role": "user", "content": "Hello"})
    conversation_history.append({"role": "assistant", "content": "Hi there!"})
    conversation_history.append({"role": "user", "content": "How are you?"})

    response = client.get('/api/stats')
    assert response.status_code == 200

    data = response.get_json()
    assert data["tasks_count"] == 2
    assert data["notes_count"] == 1
    assert data["history_length"] == 3

def test_get_stats_internal_error(client, mocker):
    mocker.patch('backend.app.datetime', mocker.MagicMock(now=mocker.MagicMock(side_effect=Exception("Test error"))))

    response = client.get('/api/stats')
    assert response.status_code == 500
    assert response.get_json()["error"] == "Test error"
