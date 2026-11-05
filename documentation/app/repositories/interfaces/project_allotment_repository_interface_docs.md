# project_allotment_repository_interface.py — File Documentation

**Original file:** `app/repositories/interfaces/project_allotment_repository_interface.py`

## Main usage
Defines method signatures that repository implementations must provide, keeping service logic independent of SQLAlchemy details.

## Why this file is needed
Repository contract keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectAllotmentRepositoryInterface`** — Abstract contract specifying which database operations the service can call.

## Functions / methods (short explanation)

- **`async ProjectAllotmentRepositoryInterface.get_project_with_members(self, project_id)`** — Loads a project together with its membership records.
- **`async ProjectAllotmentRepositoryInterface.get_membership(self, project_id, employee_id)`** — Finds an employee’s existing project allotment.
- **`async ProjectAllotmentRepositoryInterface.add_member(self, project_id, employee_id)`** — Creates a project allotment for an employee.
- **`async ProjectAllotmentRepositoryInterface.remove_member(self, allotment)`** — Marks or removes an employee’s project membership.
- **`async ProjectAllotmentRepositoryInterface.get_employee_allotments(self, employee_id)`** — Lists the projects to which an employee is allotted.

## Related project modules

Uses: `app.models.project`, `app.models.project_allotment`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
