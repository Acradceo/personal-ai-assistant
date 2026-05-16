## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-16 - Require Authentication on Chat Endpoint
**Vulnerability:** The `/api/chat` endpoint was accessible without any authentication, allowing unauthenticated users to interact with the LLM.
**Learning:** This existed because the `@require_api_key` decorator was not applied to the newly added or existing chat endpoint, despite being used on admin endpoints.
**Prevention:** Ensure all sensitive or resource-intensive endpoints explicitly include the `@require_api_key` decorator.
