# project.py — File Documentation

**Original file:** `app/api/routers/project.py`

## Main usage
Handles incoming project CRUD and project-lead change requests.

## Why this file is needed
Project endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async create_project(project, current_user, service)`** — Creates a new project after validation.
- **`async get_project_by_id(project_id, service)`** — Loads one project by ID or reports that it is missing.
- **`async get_all_projects(service, page, size)`** — Returns projects, with pagination when supported.
- **`async update_project(project_id, project, current_user, service)`** — Changes allowed project fields.
- **`async change_project_lead(project_id, data, service)`** — Assigns a different validated project lead.
- **`async delete_project(project_id, service)`** — Removes the project according to the repository/service rules.

## HTTP routes declared here

- `POST /` → `create_project()`
- `GET /{project_id}` → `get_project_by_id()`
- `GET /` → `get_all_projects()`
- `PATCH /{project_id}` → `update_project()`
- `PATCH /{project_id}/lead` → `change_project_lead()`
- `DELETE /{project_id}` → `delete_project()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.api.dependency.project_dependency`, `app.models.employee`, `app.models.project`, `app.schemas.project`, `app.services.project_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
