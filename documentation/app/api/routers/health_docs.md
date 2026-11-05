# health.py — File Documentation

**Original file:** `app/api/routers/health.py`

## Main usage
Provides basic API health and database connectivity checks.

## Why this file is needed
Health endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async health_check()`** — Checks that the API is responding.
- **`async database_health_check(db)`** — Checks that the database is reachable.

## HTTP routes declared here

- `GET /` → `health_check()`
- `GET /db` → `database_health_check()`

## Related project modules

Uses: `app.database.session`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
