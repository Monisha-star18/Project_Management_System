# employee.py — File Documentation

**Original file:** `app/api/routers/employee.py`

## Main usage
Handles incoming employee CRUD requests, validation, and responses.

## Why this file is needed
Employee endpoints keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async create_employee(employee, background_tasks, service)`** — Creates a new employee after applying layer-specific checks.
- **`async get_all_employees(page, size, service)`** — Returns employees, with pagination when supported.
- **`async get_employee_by_id(employee_id, service)`** — Loads one employee by ID or reports that it is missing.
- **`async update_employee(employee_id, employee, service)`** — Changes employee fields after validation.
- **`async delete_employee(employee_id, service)`** — Deactivates/removes an employee according to business rules.

## HTTP routes declared here

- `POST /registration` → `create_employee()`
- `GET /` → `get_all_employees()`
- `GET /{employee_id}` → `get_employee_by_id()`
- `PATCH /{employee_id}` → `update_employee()`
- `DELETE /{employee_id}` → `delete_employee()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.api.dependency.employee_dependency`, `app.models.employee`, `app.schemas.employee`, `app.services.employee_service`, `app.services.email.employee_created_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
