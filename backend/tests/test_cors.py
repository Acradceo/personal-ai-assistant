import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cors(client):
    # Test allowed origin
    headers_allowed = {'Origin': 'http://localhost:3000', 'Access-Control-Request-Method': 'GET'}
    r1 = client.options('/health', headers=headers_allowed)
    assert r1.status_code == 200
    assert r1.headers.get('Access-Control-Allow-Origin') == 'http://localhost:3000'

    # Test disallowed origin
    headers_disallowed = {'Origin': 'http://evil.com', 'Access-Control-Request-Method': 'GET'}
    r2 = client.options('/health', headers=headers_disallowed)
    assert r2.headers.get('Access-Control-Allow-Origin') != 'http://evil.com'