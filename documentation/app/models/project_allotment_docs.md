# project_allotment.py — File Documentation

**Original file:** `app/models/project_allotment.py`

## Main usage
Maps project allotment data, columns, and relationships to database tables.

## Why this file is needed
ORM database model keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectAllotment`** — SQLAlchemy model representing persisted ProjectAllotment data and its relationships.
  - Important fields: `__tablename__`, `__table_args__`, `allotment_id`, `project_id`, `employee_id`, `allotted_at`, `updated_at`, `is_active`, `remark_on_remove`, `employee`, `project`, `tasks`.

## Related project modules

Uses: `app.database.base`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
