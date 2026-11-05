# report.py — File Documentation

**Original file:** `app/api/routers/report.py`

## Main usage
Exposes calculated project summary data through an API route.

## Why this file is needed
Project reports endpoint keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async get_project_report(project_id, service)`** — Returns project membership and task progress statistics.

## HTTP routes declared here

- `GET /projects/{project_id}` → `get_project_report()`

## Related project modules

Uses: `app.api.dependency.auth`, `app.api.dependency.report_dependency`, `app.schemas.report`, `app.services.report_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
