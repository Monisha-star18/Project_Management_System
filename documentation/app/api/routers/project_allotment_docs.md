# project_allotment.py — File Documentation

**Original file:** `app/api/routers/project_allotment.py`

## Main usage
Handles adding, listing, and removing employees from projects.

## Why this file is needed
Project membership endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async add_project_employee(project_id, data, background_tasks, current_user, service, employee_service)`** — Handles an HTTP request to add a project member.
- **`async list_project_employees(project_id, service)`** — Handles an HTTP request to list project members.
- **`async get_employee_allotments(employee_id, service)`** — Lists the projects to which an employee is allotted.
- **`async remove_project_employee(project_id, employee_id, current_user, service)`** — Handles an HTTP request to remove a project member.

## HTTP routes declared here

- `POST /{project_id}/allotments` → `add_project_employee()`
- `GET /{project_id}/allotments` → `list_project_employees()`
- `GET /employees/{employee_id}/allotments` → `get_employee_allotments()`
- `DELETE /{project_id}/allotments/{employee_id}` → `remove_project_employee()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.api.dependency.project_allotment_dependency`, `app.models.employee`, `app.models.project_allotment`, `app.schemas.project_allotment`, `app.services.project_allotment_service`, `app.api.dependency.employee_dependency`, `app.services.employee_service`, `app.services.email.project_allotted_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
