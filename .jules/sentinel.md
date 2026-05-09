
## 2024-05-20 - Unauthenticated Destructive Action (Clear Data)
**Vulnerability:** The `/api/clear` endpoint in `backend/app.py` allowed any unauthenticated user to clear all backend data.
**Learning:** The endpoint lacked any authentication mechanism. Also, basic string equality (`==` or `!=`) should not be used to check sensitive tokens like API keys as it exposes the system to timing attacks.
**Prevention:** Always apply an authentication decorator (e.g., `require_api_key`) to sensitive or destructive endpoints. Always use `secrets.compare_digest()` for string comparisons involving secrets.
