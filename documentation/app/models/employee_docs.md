# employee.py — File Documentation

**Original file:** `app/models/employee.py`

## Main usage
Maps employee data, columns, and relationships to database tables.

## Why this file is needed
ORM database model keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`EmployeeData`** — SQLAlchemy model representing persisted EmployeeData data and its relationships.
  - Important fields: `__tablename__`, `__table_args__`, `employee_id`, `full_name`, `email`, `phone`, `department`, `role`, `password_hash`, `joining_date`, `is_active`, `created_at`, `led_projects`, `created_projects`, `project_allotments`, `assigned_tasks`.

## Related project modules

Uses: `app.database.base`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
