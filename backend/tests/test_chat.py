import pytest
from backend.app import app, conversation_history

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear conversation history before each test
    conversation_history.clear()
    yield
    # Clear conversation history after each test
    conversation_history.clear()

def test_chat_happy_path(client, mocker):
    mocker.patch('langchain.llms.Ollama._call', return_value="Mock response", create=True)
    mocker.patch('langchain.llms.Ollama.invoke', return_value="Mock response", create=True)
    mocked_predict = mocker.MagicMock(return_value="Mock response")
    mocker.patch('backend.app.llm', mocker.MagicMock(predict=mocked_predict))

    response = client.post('/api/chat', json={"message": "Hello"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == "Mock response"
    assert data["conversation_length"] == 2

def test_chat_empty_message(client):
    response = client.post('/api/chat', json={"message": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Empty message"

    response = client.post('/api/chat', json={"message": "   "})
    assert response.status_code == 400

def test_chat_llm_not_available(client, mocker):
    mocker.patch('backend.app.llm', None)
    response = client.post('/api/chat', json={"message": "Hello"})
    assert response.status_code == 503
    data = response.get_json()
    assert data["error"] == "Ollama LLM not available. Make sure Ollama is running."
    assert data["help"] == "Start Ollama: ollama run mistral"

def test_chat_internal_error(client, mocker):
    mocked_predict = mocker.MagicMock(side_effect=Exception('Test Error'))
    mocker.patch('backend.app.llm', mocker.MagicMock(predict=mocked_predict))

    response = client.post('/api/chat', json={"message": "Hello"})
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Test Error"
