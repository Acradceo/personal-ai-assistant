## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.

## 2026-05-12 - Missing Authentication on Admin Endpoints
**Vulnerability:** The `/api/stats` endpoint, which exposes internal application metrics like item counts and next available IDs, lacked authentication, allowing any unauthenticated user to access internal statistics.
**Learning:** This existed because the `@require_api_key` decorator was missed when the endpoint was created, despite `/api/clear` having it. This highlights a pattern where administrative or internal-facing endpoints might accidentally be left public if decorators aren't consistently applied.
**Prevention:** Always ensure that endpoints exposing internal state, statistics, or administrative actions have explicit authentication decorators (like `@require_api_key`) applied during their creation. Implement a sweeping review of all new endpoints to confirm proper authorization scopes.
