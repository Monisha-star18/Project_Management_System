# test_project_service.py — File Documentation

**Original file:** `tests/unit_tests/test_project_service.py`

## Main usage
Checks individual functions and edge cases in project service.

## Why this file is needed
Unit tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`svc()`** — Handles svc for this module.
- **`project()`** — Handles project for this module.
- **`lead()`** — Handles lead for this module.
- **`async test_create_project_commits(svc, lead, project)`** — Checks expected behavior for create project commits.
- **`async test_duplicate_project_rolls_back(svc, lead)`** — Checks error handling or rejection for duplicate project rolls back.
- **`async test_get_project_not_found(svc)`** — Checks error handling or rejection for get project not found.
- **`async test_get_project_success(svc, project)`** — Checks expected behavior for get project success.
- **`async test_get_all_projects(svc)`** — Checks expected behavior for get all projects.
- **`async test_update_project_commits(svc, project, lead)`** — Checks expected behavior for update project commits.
- **`async test_update_project_denied_for_wrong_lead(svc, project)`** — Checks error handling or rejection for update project denied for wrong lead.
- **`async test_update_project_short_duration(svc, project, lead)`** — Checks expected behavior for update project short duration.
- **`async test_update_project_duplicate_rolls_back(svc, project, lead)`** — Checks error handling or rejection for update project duplicate rolls back.
- **`async test_change_project_lead(svc, project)`** — Checks expected behavior for change project lead.
- **`async test_delete_project(svc, project)`** — Checks expected behavior for delete project.
- **`async test_delete_project_failure_rolls_back(svc, project)`** — Checks error handling or rejection for delete project failure rolls back.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.exceptions.project_exception`, `app.schemas.project`, `app.services.project_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
