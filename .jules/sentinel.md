## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-15 - Missing Authentication on Admin Endpoints
**Vulnerability:** The `/api/stats` endpoint, which exposes internal application metrics, was missing authentication (`@require_api_key`), making it publicly accessible.
**Learning:** Admin or sensitive endpoints might be added alongside protected endpoints (like `/api/clear`) but miss the required authentication decorator, creating an inconsistent security posture.
**Prevention:** Whenever adding a new endpoint under an "Admin" or sensitive grouping, explicitly verify that all required authorization and authentication decorators (like `@require_api_key`) are applied.
