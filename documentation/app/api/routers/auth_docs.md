# auth.py — File Documentation

**Original file:** `app/api/routers/auth.py`

## Main usage
Exposes login and current-user API routes.

## Why this file is needed
Authentication endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async login(form, service, description)`** — Checks account credentials and issues/returns authentication data.
- **`async get_me(current_user)`** — Gets the currently authenticated employee’s information.

## HTTP routes declared here

- `POST /login` → `login()`
- `GET /me` → `get_me()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.services.auth_service`, `app.models.employee`, `app.schemas.auth`, `app.schemas.employee`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
