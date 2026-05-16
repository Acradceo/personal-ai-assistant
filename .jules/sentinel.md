## 2026-05-09 - Overly Permissive CORS Policy
**Vulnerability:** The Flask application used `CORS(app)` without specifying allowed origins, effectively allowing any domain (`*`) to access the API.
**Learning:** This exposes the application to unauthorized data access and CSRF-like attacks from malicious websites.
**Prevention:** Always restrict CORS policies by specifying the `origins` parameter. Use environment variables (e.g., `ALLOWED_ORIGINS`) to define allowed domains dynamically, with secure defaults for local development.

## 2026-05-16 - Unauthenticated Sensitive Chat Endpoint
**Vulnerability:** The `/api/chat` endpoint, which interacts with the generative AI model, lacked authentication (`@require_api_key`), allowing unauthorized access.
**Learning:** Exposing computationally expensive endpoints like LLM inference can lead to resource exhaustion, abuse, and increased infrastructure costs. They must be secured similarly to admin endpoints.
**Prevention:** Apply strict authentication (e.g., `@require_api_key`) and potentially rate-limiting to all endpoints that consume significant resources or interact with generative AI.
