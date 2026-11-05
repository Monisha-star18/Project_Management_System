# project_allotment.py — File Documentation

**Original file:** `app/schemas/project_allotment.py`

## Main usage
Defines validated request and response structures for project allotment operations.

## Why this file is needed
API data schema keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`AllotmentCreate`** — Pydantic schema for validating or serializing allotment creation input.
  - Important fields: `model_config`, `employee_id`.
- **`AllottedEmployeeResponse`** — Pydantic schema for validating or serializing allottedemployee responses.
  - Important fields: `model_config`, `employee_id`, `full_name`, `role`.
- **`AllotmentResponse`** — Pydantic schema for validating or serializing allotment responses.
  - Important fields: `model_config`, `allotment_id`, `project_id`, `employee_id`, `employee_name`, `role`.
- **`AllotmentListResponse`** — Pydantic schema for validating or serializing allotmentlist responses.
  - Important fields: `project_id`, `total`, `members`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
