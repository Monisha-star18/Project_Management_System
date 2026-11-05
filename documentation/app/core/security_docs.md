# security.py — File Documentation

**Original file:** `app/core/security.py`

## Main usage
Hashes and verifies passwords and creates/decodes JWT access tokens.

## Why this file is needed
Authentication utilities keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`hash_password(password)`** — Converts a plain-text password to a secure stored hash.
- **`verify_password(plain_password, hashed_password)`** — Checks a plain-text password against its stored hash.
- **`create_access_token(email_id)`** — Signs a JWT access token with configured expiration.
- **`decode_access_token(token)`** — Validates and decodes a JWT token.

## Related project modules

Uses: `app.core.config`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
