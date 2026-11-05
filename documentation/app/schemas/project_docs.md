# project.py — File Documentation

**Original file:** `app/schemas/project.py`

## Main usage
Defines validated request and response structures for project operations.

## Why this file is needed
API data schema keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectCreate`** — Pydantic schema for validating or serializing project creation input.
  - Important fields: `model_config`, `project_name`, `project_description`, `lead_id`, `start_date`, `expected_end_date`.
- **`ProjectUpdate`** — Pydantic schema for validating or serializing project update input.
  - Important fields: `model_config`, `project_name`, `project_description`, `start_date`, `expected_end_date`, `status`.
- **`ProjectLeadUpdate`** — Pydantic schema for validating or serializing projectlead update input.
  - Important fields: `model_config`, `lead_id`, `remark_on_remove`.
- **`ProjectResponse`** — Pydantic schema for validating or serializing project responses.
  - Important fields: `model_config`, `project_id`, `project_name`, `project_description`, `lead_id`, `start_date`, `expected_end_date`, `status`, `created_by`, `created_at`, `updated_at`.
- **`PaginatedProjectResponse`** — Pydantic schema for validating or serializing paginatedproject responses.
  - Important fields: `pages`, `projects`.

## Functions / methods (short explanation)

- **`ProjectCreate.validate_dates(self)`** — Validates project start and end dates.
- **`ProjectUpdate.validate_dates(self)`** — Validates project start and end dates.

## Related project modules

Uses: `app.exceptions.project_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
