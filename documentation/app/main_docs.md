# main.py — File Documentation

**Original file:** `app/main.py`

## Main usage
Creates the FastAPI application, registers routers and middleware, handles application errors, and runs startup/shutdown tasks.

## Why this file is needed
Application entry point keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async lifespan(app)`** — Runs application startup setup and shutdown cleanup.
- **`async root()`** — Returns a welcome message from the root API.

## Related project modules

Uses: `app.core.config`, `app.api.routers.health`, `app.api.routers.employee`, `app.api.routers.auth`, `app.api.routers.project`, `app.api.routers.project_allotment`, `app.api.routers.task`, `app.api.routers.report`, `app.exceptions.base_exception`, `app.exceptions.handlers`, `app.utilites.logger`, `app.middleware.logging_middleware`, `app.scripts.create_admin`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
