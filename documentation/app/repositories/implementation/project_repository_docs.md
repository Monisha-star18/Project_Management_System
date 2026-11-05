# project_repository.py — File Documentation

**Original file:** `app/repositories/implementation/project_repository.py`

## Main usage
Implements persistence operations and database queries for project.

## Why this file is needed
Database repository keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectRepository`** — Concrete SQLAlchemy implementation of the repository contract.

## Functions / methods (short explanation)

- **`ProjectRepository.__init__(self, db)`** — Stores dependencies or initializes an object.
- **`async ProjectRepository.create_new_project(self, project, created_by)`** — Creates new project and returns the result.
- **`async ProjectRepository.get_project_by_id(self, project_id)`** — Loads one project by ID or reports that it is missing.
- **`async ProjectRepository.get_all_projects(self, page, size)`** — Returns projects, with pagination when supported.
- **`async ProjectRepository.update_project(self, project, data)`** — Changes allowed project fields.
- **`async ProjectRepository.delete_project(self, project)`** — Removes the project according to the repository/service rules.

## Related project modules

Uses: `app.models.project`, `app.models.project_allotment`, `app.repositories.interfaces.project_repository_interface`, `app.schemas.project`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
