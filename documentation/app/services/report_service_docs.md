# report_service.py — File Documentation

**Original file:** `app/services/report_service.py`

## Main usage
Calculates active member counts, task totals, completed tasks, completion percentage, and average progress.

## Why this file is needed
Project reporting business logic keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ReportService`** — Business logic component that enforces application rules and coordinates database operations.

## Functions / methods (short explanation)

- **`ReportService.__init__(self, repository)`** — Stores dependencies or initializes an object.
- **`async ReportService.get_project_report(self, project_id)`** — Returns project membership and task progress statistics.

## Related project modules

Uses: `app.exceptions.project_exception`, `app.repositories.interfaces.report_repository_interface`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
