# project_repository_interface.py — File Documentation

**Original file:** `app/repositories/interfaces/project_repository_interface.py`

## Main usage
Defines method signatures that repository implementations must provide, keeping service logic independent of SQLAlchemy details.

## Why this file is needed
Repository contract keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectRepositoryInterface`** — Abstract contract specifying which database operations the service can call.

## Functions / methods (short explanation)

- **`async ProjectRepositoryInterface.create_new_project(self, project, created_by)`** — Creates new project and returns the result.
- **`async ProjectRepositoryInterface.get_project_by_id(self, project_id)`** — Loads one project by ID or reports that it is missing.
- **`async ProjectRepositoryInterface.get_all_projects(self, page, size, lead_id, created_by, member_employee_id)`** — Returns projects, with pagination when supported.
- **`async ProjectRepositoryInterface.update_project(self, project, data)`** — Changes allowed project fields.
- **`async ProjectRepositoryInterface.delete_project(self, project)`** — Removes the project according to the repository/service rules.

## Related project modules

Uses: `app.models.project`, `app.schemas.project`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
