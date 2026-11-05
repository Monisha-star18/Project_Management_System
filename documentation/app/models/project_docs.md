# project.py — File Documentation

**Original file:** `app/models/project.py`

## Main usage
Maps project data, columns, and relationships to database tables.

## Why this file is needed
ORM database model keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectDetails`** — SQLAlchemy model representing persisted ProjectDetails data and its relationships.
  - Important fields: `__tablename__`, `__table_args__`, `project_id`, `project_name`, `project_description`, `lead_id`, `start_date`, `expected_end_date`, `status`, `created_by`, `created_at`, `updated_at`, `lead`, `creator`, `allotments`.

## Related project modules

Uses: `app.database.base`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
