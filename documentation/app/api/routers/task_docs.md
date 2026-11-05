# task.py — File Documentation

**Original file:** `app/api/routers/task.py`

## Main usage
Exposes task assignment, querying, updates, progress, and deletion routes.

## Why this file is needed
Task endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async create_task(project_id, data, background_tasks, current_user, service, employee_service)`** — Creates task and returns the result.
- **`async list_project_tasks(project_id, current_user, service)`** — Returns the requested list of project tasks.
- **`async get_task(task_id, current_user, service)`** — Loads a task by its identifier.
- **`async get_my_tasks(current_user, service)`** — Returns the authenticated employee’s tasks.
- **`async get_employee_project_tasks(project_id, employee_id, current_user, service)`** — Returns an employee’s tasks in a project.
- **`async update_task(task_id, data, current_user, service)`** — Applies changes to task.
- **`async update_task_progress(task_id, data, current_user, service)`** — Handles an HTTP request to update task progress.
- **`async delete_task(task_id, current_user, service)`** — Deletes the selected task record.

## HTTP routes declared here

- `POST /projects/{project_id}/tasks` → `create_task()`
- `GET /projects/{project_id}/tasks` → `list_project_tasks()`
- `GET /tasks/{task_id}` → `get_task()`
- `GET /employees/me/tasks` → `get_my_tasks()`
- `GET /projects/{project_id}/employees/{employee_id}/tasks` → `get_employee_project_tasks()`
- `PATCH /tasks/{task_id}` → `update_task()`
- `PATCH /tasks/{task_id}/progress` → `update_task_progress()`
- `DELETE /tasks/{task_id}` → `delete_task()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.api.dependency.task_dependency`, `app.models.employee`, `app.schemas.task`, `app.services.task_service`, `app.api.dependency.employee_dependency`, `app.services.employee_service`, `app.services.email.task_assigned_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
