# test_project_api.py — File Documentation

**Original file:** `tests/api/test_project_api.py`

## Main usage
Checks HTTP endpoints for expected successful and unsuccessful project api behavior.

## Why this file is needed
API integration tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`project_data(lead_id)`** — Handles project data for this module.
- **`async create_project(client, auth_headers, admin)`** — Creates a new project after validation.
- **`async test_create_project_valid(client, auth_headers, admin)`** — Checks expected behavior for create project valid.
- **`async test_create_project_invalid(client, auth_headers, admin)`** — Checks error handling or rejection for create project invalid.
- **`async test_get_all_projects_valid(client, auth_headers)`** — Checks expected behavior for get all projects valid.
- **`async test_get_all_projects_invalid(client, auth_headers)`** — Checks error handling or rejection for get all projects invalid.
- **`async test_get_project_valid(client, auth_headers, admin)`** — Checks expected behavior for get project valid.
- **`async test_get_project_invalid(client, auth_headers)`** — Checks error handling or rejection for get project invalid.
- **`async test_update_project_valid(client, auth_headers, admin)`** — Checks expected behavior for update project valid.
- **`async test_update_project_invalid(client, auth_headers, admin)`** — Checks error handling or rejection for update project invalid.
- **`async test_change_project_lead_valid(client, auth_headers, admin, test_session)`** — Checks expected behavior for change project lead valid.
- **`async test_change_project_lead_invalid(client, auth_headers, admin)`** — Checks error handling or rejection for change project lead invalid.
- **`async test_delete_project_valid(client, auth_headers, admin)`** — Checks expected behavior for delete project valid.
- **`async test_delete_project_invalid(client, auth_headers)`** — Checks error handling or rejection for delete project invalid.

## Related project modules

Uses: `app.models.employee`, `app.core.security`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
