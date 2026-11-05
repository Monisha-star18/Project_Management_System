# task.py — File Documentation

**Original file:** `app/models/task.py`

## Main usage
Maps task data, columns, and relationships to database tables.

## Why this file is needed
ORM database model keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskDetails`** — SQLAlchemy model representing persisted TaskDetails data and its relationships.
  - Important fields: `__tablename__`, `__table_args__`, `task_id`, `allotment_id`, `task_title`, `description`, `assigned_by`, `priority`, `start_date`, `due_date`, `status`, `progress_percentage`, `remarks`, `created_at`, `updated_at`, `allotment`, `assigner`.

## Related project modules

Uses: `app.database.base`, `app.models.employee`, `app.models.project_allotment`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
