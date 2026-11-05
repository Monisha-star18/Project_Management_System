# task.py — File Documentation

**Original file:** `app/schemas/task.py`

## Main usage
Defines validated request and response structures for task operations.

## Why this file is needed
API data schema keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskCreate`** — Pydantic schema for validating or serializing task creation input.
  - Important fields: `model_config`, `employee_id`, `task_title`, `description`, `priority`, `start_date`, `due_date`.
- **`TaskUpdate`** — Pydantic schema for validating or serializing task update input.
  - Important fields: `model_config`, `employee_id`, `task_title`, `description`, `priority`, `start_date`, `due_date`, `remarks`.
- **`TaskProgressUpdate`** — Pydantic schema for validating or serializing taskprogress update input.
  - Important fields: `model_config`, `progress_percentage`, `status`, `remarks`.
- **`TaskResponse`** — Pydantic schema for validating or serializing task responses.
  - Important fields: `model_config`, `task_id`, `allotment_id`, `project_id`, `employee_id`, `task_title`, `description`, `assigned_by`, `priority`, `start_date`, `due_date`, `status`, `progress_percentage`, `remarks`, `created_at`, `updated_at`.

## Functions / methods (short explanation)

- **`TaskCreate.check_dates(self)`** — Validates the task date constraints.
- **`TaskProgressUpdate.check_progress(self)`** — Validates the submitted task progress value.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
