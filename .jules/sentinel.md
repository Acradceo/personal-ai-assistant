## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-15 - Missing Authentication on Task Endpoints
**Vulnerability:** The `/api/tasks` and `/api/tasks/<int:task_id>` endpoints lacked authentication, allowing unauthorized users to read, create, update, and delete tasks.
**Learning:** This occurred because the `@require_api_key` decorator, although present in the codebase, was not applied to the newly created task management endpoints.
**Prevention:** Ensure all non-public API endpoints explicitly implement authentication mechanisms (like the `@require_api_key` decorator) during creation.
