# conftest.py — File Documentation

**Original file:** `tests/conftest.py`

## Main usage
Sets up test database sessions, HTTP client, sample users, and authentication fixtures.

## Why this file is needed
Shared test fixtures keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async test_engine()`** — Checks expected behavior for engine.
- **`async test_session(test_engine)`** — Checks expected behavior for session.
- **`async client(test_session)`** — Handles client for this module.
- **`async admin(test_session)`** — Handles admin for this module.
- **`async auth_headers(admin)`** — Handles auth headers for this module.
- **`async team_lead(test_session)`** — Handles team lead for this module.
- **`async lead_headers(team_lead)`** — Handles lead headers for this module.

## Related project modules

Uses: `app.core.config`, `app.database.base`, `app.database.session`, `app.main`, `app.models.employee`, `app.core.security`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
