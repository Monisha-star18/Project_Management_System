# task_dependency.py — File Documentation

**Original file:** `app/api/dependency/task_dependency.py`

## Main usage
Creates repository and service objects needed by API routes so route handlers stay small and testable.

## Why this file is needed
Dependency injection keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`get_task_repository(db)`** — Provides a repository instance through FastAPI dependency injection.
- **`get_task_service(repository, db)`** — Provides a service instance with its required repository and session.

## Related project modules

Uses: `app.database.session`, `app.repositories.implementation.task_repository`, `app.repositories.interfaces.task_repository_interface`, `app.services.task_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
