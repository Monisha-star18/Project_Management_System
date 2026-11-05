# task_repository.py — File Documentation

**Original file:** `app/repositories/implementation/task_repository.py`

## Main usage
Implements persistence operations and database queries for task.

## Why this file is needed
Database repository keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskRepository`** — Concrete SQLAlchemy implementation of the repository contract.

## Functions / methods (short explanation)

- **`TaskRepository.__init__(self, db)`** — Stores dependencies or initializes an object.
- **`async TaskRepository.get_project(self, project_id)`** — Loads a project required for subsequent processing.
- **`async TaskRepository.get_allotment(self, project_id, employee_id)`** — Loads a project–employee allotment.
- **`async TaskRepository.get_task(self, task_id)`** — Loads a task by its identifier.
- **`async TaskRepository.list_tasks(self, project_id, employee_id)`** — Queries tasks using the supplied filters.
- **`async TaskRepository.add_task(self, task)`** — Persists a new task record.
- **`async TaskRepository.delete_task(self, task)`** — Deletes the selected task record.

## Related project modules

Uses: `app.models.project`, `app.models.project_allotment`, `app.models.task`, `app.repositories.interfaces.task_repository_interface`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
