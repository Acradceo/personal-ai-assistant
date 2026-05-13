## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-13 - Missing Authentication on Admin Endpoint
**Vulnerability:** The `/api/stats` endpoint exposed internal application statistics (task/note counts, last IDs) without requiring authentication, while the nearby `/api/clear` endpoint was correctly protected.
**Learning:** Admin endpoints grouped together may accidentally omit authentication decorators if not systematically reviewed.
**Prevention:** Apply decorators consistently across all endpoints within the same functional or administrative grouping.
