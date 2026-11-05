# project_allotment_service.py — File Documentation

**Original file:** `app/services/project_allotment_service.py`

## Main usage
Adds, lists, and removes project members while enforcing lead permissions, employee eligibility, and uniqueness.

## Why this file is needed
Project membership business logic keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectAllotmentService`** — Business logic component that enforces application rules and coordinates database operations.

## Functions / methods (short explanation)

- **`ProjectAllotmentService.__init__(self, repository, employee_repository, db)`** — Stores dependencies or initializes an object.
- **`ProjectAllotmentService._check_project_lead(current_user, project)`** — Checks that the current user is the active project lead.
- **`async ProjectAllotmentService.add_employee(self, project_id, data, current_user)`** — Adds an eligible employee to a project.
- **`async ProjectAllotmentService.list_members(self, project_id)`** — Lists active employees assigned to a project.
- **`async ProjectAllotmentService.remove_employee(self, project_id, employee_id, current_user)`** — Removes a project member after authorization checks.
- **`async ProjectAllotmentService.get_employee_allotments(self, employee_id)`** — Lists the projects to which an employee is allotted.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.exceptions.employee_exception`, `app.exceptions.project_allotment_exception`, `app.models.employee`, `app.models.project`, `app.models.project_allotment`, `app.repositories.interfaces.employee_repository_interface`, `app.repositories.interfaces.project_allotment_repository_interface`, `app.schemas.project_allotment`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
