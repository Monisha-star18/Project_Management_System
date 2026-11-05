# auth_exception.py — File Documentation

**Original file:** `app/exceptions/auth_exception.py`

## Main usage
Defines meaningful application errors for auth exception failures instead of generic exceptions.

## Why this file is needed
Domain-specific exceptions keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`InvalidCredentialsError`** — Custom error raised when invalid credentials occurs.
- **`InactiveUserError`** — Custom error raised when inactive user occurs.
- **`PermissionDeniedError`** — Custom error raised when permission denied occurs.
- **`InvalidTokenError`** — Custom error raised when invalid token occurs.

## Functions / methods (short explanation)

- **`InvalidCredentialsError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InactiveUserError.__init__(self)`** — Stores dependencies or initializes an object.
- **`PermissionDeniedError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InvalidTokenError.__init__(self)`** — Stores dependencies or initializes an object.

## Related project modules

Uses: `app.exceptions.base_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
