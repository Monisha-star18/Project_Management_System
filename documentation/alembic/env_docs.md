# env.py — File Documentation

**Original file:** `alembic/env.py`

## Main usage
Connects Alembic to SQLAlchemy metadata and runs migrations in online or offline modes.

## Why this file is needed
Migration environment keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`run_migrations_offline()`** — Generates migration SQL without connecting to a database.
- **`do_run_migrations(connection)`** — Runs migrations on the provided database connection.
- **`async run_async_migrations()`** — Opens an async connection to execute migrations.
- **`run_migrations_online()`** — Runs migrations against a live database.

## Related project modules

Uses: `app.core.config`, `app.database.base`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
