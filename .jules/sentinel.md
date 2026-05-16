## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.
## 2024-05-16 - Data Exposure in Exception Handlers
**Vulnerability:** Raw exception messages (`str(e)`) were being returned directly in 500 API responses.
**Learning:** This exposes internal server details and logic to the client, leading to potential data exposure.
**Prevention:** Always log the actual error internally (`logger.error(e)`) and return a generic, safe error message like `"An internal error occurred"` to the client.
