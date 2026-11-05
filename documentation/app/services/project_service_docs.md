# project_service.py — File Documentation

**Original file:** `app/services/project_service.py`

## Main usage
Creates and manages projects, validates leads and permissions, and enforces project rules.

## Why this file is needed
Project business logic keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectService`** — Business logic component that enforces application rules and coordinates database operations.

## Functions / methods (short explanation)

- **`ProjectService.__init__(self, repository, employee_repository, db)`** — Stores dependencies or initializes an object.
- **`ProjectService._check_project_lead(current_user, project)`** — Checks that the current user is the active project lead.
- **`async ProjectService._validate_lead(self, lead_id)`** — Validates whether an employee can lead a project.
- **`async ProjectService.create_project(self, project, current_user)`** — Creates a new project after validation.
- **`async ProjectService.get_project_by_id(self, project_id)`** — Loads one project by ID or reports that it is missing.
- **`async ProjectService.get_all_projects(self, page, size)`** — Returns projects, with pagination when supported.
- **`async ProjectService.update_project(self, project_id, data, current_user)`** — Changes allowed project fields.
- **`async ProjectService.change_project_lead(self, project_id, data)`** — Assigns a different validated project lead.
- **`async ProjectService.delete_project(self, project_id)`** — Removes the project according to the repository/service rules.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.exceptions.project_exception`, `app.models.employee`, `app.models.project`, `app.models.project_allotment`, `app.repositories.interfaces.employee_repository_interface`, `app.repositories.interfaces.project_repository_interface`, `app.schemas.project`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
