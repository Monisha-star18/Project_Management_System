# create_admin.py — File Documentation

**Original file:** `app/scripts/create_admin.py`

## Main usage
Creates the initial admin account when needed.

## Why this file is needed
Admin initialization keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async create_admin()`** — Creates or ensures a seeded admin user exists.

## Related project modules

Uses: `app.core.config`, `app.core.security`, `app.database.session`, `app.models.employee`, `app.utilites.logger`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
