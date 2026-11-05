# test_auth_service.py — File Documentation

**Original file:** `tests/unit_tests/test_auth_service.py`

## Main usage
Checks individual functions and edge cases in auth service.

## Why this file is needed
Unit tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`svc()`** — Handles svc for this module.
- **`user()`** — Handles user for this module.
- **`async test_login_success(svc, user, monkeypatch)`** — Checks expected behavior for login success.
- **`async test_login_user_not_found(svc)`** — Checks error handling or rejection for login user not found.
- **`async test_login_wrong_password(svc, user, monkeypatch)`** — Checks error handling or rejection for login wrong password.
- **`async test_login_inactive_user(svc, user, monkeypatch)`** — Checks expected behavior for login inactive user.
- **`async test_get_me_success(svc, user, monkeypatch)`** — Checks expected behavior for get me success.
- **`async test_get_me_invalid_token(svc, monkeypatch)`** — Checks error handling or rejection for get me invalid token.
- **`async test_get_me_user_not_found(svc, monkeypatch)`** — Checks error handling or rejection for get me user not found.
- **`async test_get_me_inactive_user(svc, user, monkeypatch)`** — Checks expected behavior for get me inactive user.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.services.auth_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
