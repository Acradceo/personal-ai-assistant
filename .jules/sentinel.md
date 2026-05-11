## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.

## 2026-05-11 - Missing Authentication on Internal Endpoints
**Vulnerability:** The `/api/stats` endpoint, intended for administrative use and exposing sensitive application state (counts, IDs), lacked the `@require_api_key` decorator, allowing unauthenticated access.
**Learning:** In Flask applications where decorators are used for authentication, it's easy to omit them when adding new endpoints, especially if they are structurally grouped but not programmatically protected (e.g., in a blueprint or class).
**Prevention:** Consistently apply authentication decorators like `@require_api_key` to all sensitive and administrative endpoints. Automated testing should explicitly verify that these endpoints enforce authentication by simulating requests with and without valid credentials.
