# auth.py — File Documentation

**Original file:** `app/api/dependency/auth.py`

## Main usage
Creates repository and service objects needed by API routes so route handlers stay small and testable.

## Why this file is needed
Dependency injection keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`get_auth_repository(db)`** — Provides a repository instance through FastAPI dependency injection.
- **`get_auth_service(repository)`** — Provides a service instance with its required repository and session.
- **`async get_current_user(token, service)`** — Reads and validates the access token and resolves the logged-in user.
- **`require_roles(*allowed_roles)`** — Restricts an endpoint to permitted user roles.

## Related project modules

Uses: `app.database.session`, `app.exceptions.auth_exception`, `app.models.employee`, `app.repositories.implementation.auth_repository`, `app.repositories.interfaces.auth_repository_interface`, `app.services.auth_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
