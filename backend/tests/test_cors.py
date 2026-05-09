import requests
import sys
import time

def test_cors():
    # Wait for server to start if not already
    time.sleep(1)

    # Test allowed origin
    print("Testing allowed origin: http://localhost:3000...")
    headers_allowed = {'Origin': 'http://localhost:3000', 'Access-Control-Request-Method': 'GET'}
    r1 = requests.options('http://localhost:5000/health', headers=headers_allowed)
    if r1.status_code != 200 or r1.headers.get('Access-Control-Allow-Origin') != 'http://localhost:3000':
        print(f"Failed allowed origin test. Headers: {r1.headers}")
        sys.exit(1)
    print("Passed allowed origin test.")

    # Test disallowed origin
    print("Testing disallowed origin: http://evil.com...")
    headers_disallowed = {'Origin': 'http://evil.com', 'Access-Control-Request-Method': 'GET'}
    r2 = requests.options('http://localhost:5000/health', headers=headers_disallowed)
    if r2.headers.get('Access-Control-Allow-Origin') == 'http://evil.com':
        print(f"Failed disallowed origin test. Headers: {r2.headers}")
        sys.exit(1)
    print("Passed disallowed origin test.")

    print("All CORS tests passed!")

if __name__ == '__main__':
    test_cors()