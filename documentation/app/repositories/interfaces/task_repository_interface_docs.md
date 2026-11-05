# task_repository_interface.py — File Documentation

**Original file:** `app/repositories/interfaces/task_repository_interface.py`

## Main usage
Defines method signatures that repository implementations must provide, keeping service logic independent of SQLAlchemy details.

## Why this file is needed
Repository contract keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskRepositoryInterface`** — Abstract contract specifying which database operations the service can call.

## Functions / methods (short explanation)

- **`async TaskRepositoryInterface.get_project(self, project_id)`** — Loads a project required for subsequent processing.
- **`async TaskRepositoryInterface.get_allotment(self, project_id, employee_id)`** — Loads a project–employee allotment.
- **`async TaskRepositoryInterface.get_task(self, task_id)`** — Loads a task by its identifier.
- **`async TaskRepositoryInterface.list_tasks(self, project_id, employee_id)`** — Queries tasks using the supplied filters.
- **`async TaskRepositoryInterface.add_task(self, task)`** — Persists a new task record.
- **`async TaskRepositoryInterface.delete_task(self, task)`** — Deletes the selected task record.

## Related project modules

Uses: `app.models.project`, `app.models.project_allotment`, `app.models.task`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
