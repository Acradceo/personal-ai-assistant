## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-16 - Add Authentication to Notes Endpoints
**Vulnerability:** Missing authentication on the `/api/notes` and `/api/notes/<int:note_id>` endpoints allowed unauthorized access (read, create, update, delete) to notes.
**Learning:** The `@require_api_key` decorator was present in the codebase but missing from these specific route handlers.
**Prevention:** Ensure all sensitive endpoints are explicitly protected with the `@require_api_key` decorator during route creation. Include authentication enforcement checks in the test suite for all endpoints.
