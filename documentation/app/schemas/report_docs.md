# report.py — File Documentation

**Original file:** `app/schemas/report.py`

## Main usage
Defines validated request and response structures for report operations.

## Why this file is needed
API data schema keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectReportResponse`** — Pydantic schema for validating or serializing projectreport responses.
  - Important fields: `project`, `total_employees`, `total_tasks`, `completed_tasks`, `completion_percentage`, `overall_progress_percentage`.

## Related project modules

Uses: `app.schemas.project`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
