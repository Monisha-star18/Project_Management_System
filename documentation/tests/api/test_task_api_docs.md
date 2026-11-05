# test_task_api.py — File Documentation

**Original file:** `tests/api/test_task_api.py`

## Main usage
Checks HTTP endpoints for expected successful and unsuccessful task api behavior.

## Why this file is needed
API integration tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`async setup_project(client, auth_headers, lead_headers, team_lead, test_session)`** — Handles setup project for this module.
- **`task_data(employee_id)`** — Handles task data for this module.
- **`async setup_task(client, auth_headers, lead_headers, team_lead, test_session)`** — Handles setup task for this module.
- **`async test_create_task_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for create task valid.
- **`async test_create_task_invalid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks error handling or rejection for create task invalid.
- **`async test_list_project_tasks_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for list project tasks valid.
- **`async test_list_project_tasks_invalid(client, lead_headers)`** — Checks error handling or rejection for list project tasks invalid.
- **`async test_get_task_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for get task valid.
- **`async test_get_task_invalid(client, lead_headers)`** — Checks error handling or rejection for get task invalid.
- **`async test_get_my_tasks_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for get my tasks valid.
- **`async test_get_my_tasks_invalid(client, auth_headers)`** — Checks error handling or rejection for get my tasks invalid.
- **`async test_employee_project_tasks_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for employee project tasks valid.
- **`async test_employee_project_tasks_invalid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks error handling or rejection for employee project tasks invalid.
- **`async test_update_task_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for update task valid.
- **`async test_update_task_invalid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks error handling or rejection for update task invalid.
- **`async test_update_progress_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for update progress valid.
- **`async test_update_progress_invalid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks error handling or rejection for update progress invalid.
- **`async test_delete_task_valid(client, auth_headers, lead_headers, team_lead, test_session)`** — Checks expected behavior for delete task valid.
- **`async test_delete_task_invalid(client, lead_headers)`** — Checks error handling or rejection for delete task invalid.

## Related project modules

Uses: `app.models.employee`, `app.core.security`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
