# config.py — File Documentation

**Original file:** `app/core/config.py`

## Main usage
Loads typed database, JWT, admin, and email settings from environment variables.

## Why this file is needed
Configuration management keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`Settings`** — Groups related behavior and data for this file.

## Functions / methods (short explanation)

- **`Settings.database_url(self)`** — Builds the async PostgreSQL connection URL.
- **`Settings.test_database_url(self)`** — Builds a separate PostgreSQL connection URL for tests.
- **`get_settings()`** — Returns cached environment-backed application settings.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
