import pytest
from backend.app import app, get_cached_llm_response

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cache(client, mocker):
    # Clear cache before testing
    get_cached_llm_response.cache_clear()

    mocked_predict = mocker.MagicMock(return_value="Mock response")
    mocker.patch('backend.app.llm', mocker.MagicMock(predict=mocked_predict))

    # First call
    response1 = client.post('/api/chat', json={"message": "Hello Cache"})
    assert response1.get_json()["response"] == "Mock response"

    # Second call (should hit cache)
    response2 = client.post('/api/chat', json={"message": "Hello Cache"})
    assert response2.get_json()["response"] == "Mock response"

    # Third call (different message, shouldn't hit cache)
    response3 = client.post('/api/chat', json={"message": "Different Message"})
    assert response3.get_json()["response"] == "Mock response"

    # llm.predict should only have been called twice (once for "Hello Cache", once for "Different Message")
    assert mocked_predict.call_count == 2
