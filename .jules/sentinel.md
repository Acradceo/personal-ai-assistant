## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2026-05-14 - Add authentication to admin endpoint
**Vulnerability:** The `/api/stats` endpoint, an admin endpoint, lacked authentication and exposed internal data unconditionally.
**Learning:** This exposes data to unauthorized users. It's critical to ensure all sensitive endpoints use proper authentication mechanisms. In this codebase, the `@require_api_key` decorator exists to solve this problem but was missing from `/api/stats`.
**Prevention:** Check for `@require_api_key` on all endpoints categorized under 'Admin Endpoints' or handling sensitive data. Ensure new endpoints handling internal data also implement this authorization check.
