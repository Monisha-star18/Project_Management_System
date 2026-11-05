# employee_repository.py — File Documentation

**Original file:** `app/repositories/implementation/employee_repository.py`

## Main usage
Implements persistence operations and database queries for employee.

## Why this file is needed
Database repository keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`EmployeeRepository`** — Concrete SQLAlchemy implementation of the repository contract.

## Functions / methods (short explanation)

- **`EmployeeRepository.__init__(self, db)`** — Stores dependencies or initializes an object.
- **`async EmployeeRepository.create_new_employee(self, employee)`** — Creates new employee and returns the result.
- **`async EmployeeRepository.get_all_employees(self, page, size)`** — Returns employees, with pagination when supported.
- **`async EmployeeRepository.get_employee_by_id(self, employee_id)`** — Loads one employee by ID or reports that it is missing.
- **`async EmployeeRepository.update_employee(self, employee, data)`** — Changes employee fields after validation.
- **`async EmployeeRepository.soft_delete_employee(self, employee)`** — Marks an employee inactive instead of physically deleting the record.

## Related project modules

Uses: `app.core.security`, `app.models.employee`, `app.repositories.interfaces.employee_repository_interface`, `app.schemas.employee`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
