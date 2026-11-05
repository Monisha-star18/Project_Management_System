# task_service.py — File Documentation

**Original file:** `app/services/task_service.py`

## Main usage
Creates, assigns, lists, updates, and deletes tasks with project membership checks and permission rules.

## Why this file is needed
Task business logic keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskService`** — Business logic component that enforces application rules and coordinates database operations.

## Functions / methods (short explanation)

- **`TaskService.__init__(self, repository, db)`** — Stores dependencies or initializes an object.
- **`TaskService._lead(self, user, project)`** — Checks whether the user is the active lead for the requested project.
- **`async TaskService._project(self, project_id)`** — Loads a project or raises a not-found error.
- **`async TaskService._task(self, task_id)`** — Loads a task or raises a not-found error.
- **`async TaskService._allotment(self, project_id, employee_id)`** — Loads an employee’s project membership or rejects invalid assignment.
- **`TaskService._response(task)`** — Builds a validated task API response from ORM data.
- **`async TaskService.create(self, project_id, data, user)`** — Creates and saves a new record.
- **`async TaskService.list_project(self, project_id, user)`** — Lists tasks belonging to the selected project.
- **`async TaskService.get(self, task_id, user)`** — Retrieves the requested record with access checks.
- **`async TaskService.mine(self, user)`** — Returns tasks assigned to the current user.
- **`async TaskService.project_employee(self, project_id, employee_id, user)`** — Returns an employee’s tasks for a selected project.
- **`async TaskService.update(self, task_id, data, user)`** — Applies validated changes to an existing record.
- **`async TaskService.progress(self, task_id, data, user)`** — Updates a task’s progress/status according to business rules.
- **`async TaskService.delete(self, task_id, user)`** — Deletes/removes the requested record after checks.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.exceptions.project_exception`, `app.exceptions.task_exception`, `app.models.employee`, `app.models.project`, `app.models.task`, `app.repositories.interfaces.task_repository_interface`, `app.schemas.task`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
