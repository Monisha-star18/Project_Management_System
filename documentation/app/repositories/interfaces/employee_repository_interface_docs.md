# employee_repository_interface.py — File Documentation

**Original file:** `app/repositories/interfaces/employee_repository_interface.py`

## Main usage
Defines method signatures that repository implementations must provide, keeping service logic independent of SQLAlchemy details.

## Why this file is needed
Repository contract keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`EmployeeRepositoryInterface`** — Abstract contract specifying which database operations the service can call.

## Functions / methods (short explanation)

- **`async EmployeeRepositoryInterface.create_new_employee(self, employee)`** — Creates new employee and returns the result.
- **`async EmployeeRepositoryInterface.get_all_employees(self, page, size)`** — Returns employees, with pagination when supported.
- **`async EmployeeRepositoryInterface.get_employee_by_id(self, employee_id)`** — Loads one employee by ID or reports that it is missing.
- **`async EmployeeRepositoryInterface.update_employee(self, employee, data)`** — Changes employee fields after validation.
- **`async EmployeeRepositoryInterface.soft_delete_employee(self, employee)`** — Marks an employee inactive instead of physically deleting the record.

## Related project modules

Uses: `app.models.employee`, `app.schemas.employee`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
