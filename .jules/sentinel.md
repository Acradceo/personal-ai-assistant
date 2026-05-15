## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.

## 2026-05-10 - Missing Authentication on Admin Endpoint
**Vulnerability:** The `/api/stats` admin endpoint was missing the `@require_api_key` decorator, allowing unauthenticated access to system statistics.
**Learning:** In Flask, route decorators must be consistently applied to all sensitive endpoints. Failing to do so can expose internal state.
**Prevention:** Always verify that endpoints intended for admin or internal use have the appropriate authentication decorators explicitly applied during code reviews and testing.
