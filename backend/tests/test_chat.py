import pytest
import json
import sys
import os

# Add the backend directory to the Python path so app can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chat_empty_message(client):
    """Test that submitting an empty message returns a 400 error."""
    # Test with empty string
    response = client.post(
        '/api/chat',
        data=json.dumps({"message": ""}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Empty message"

    # Test with string containing only whitespace
    response = client.post(
        '/api/chat',
        data=json.dumps({"message": "   "}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Empty message"

def test_chat_missing_message_field(client):
    """Test that submitting a request without the message field returns a 400 error."""
    response = client.post(
        '/api/chat',
        data=json.dumps({"not_message": "hello"}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Empty message"
