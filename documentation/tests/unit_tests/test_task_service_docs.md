# test_task_service.py — File Documentation

**Original file:** `tests/unit_tests/test_task_service.py`

## Main usage
Checks individual functions and edge cases in task service.

## Why this file is needed
Unit tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`svc()`** — Handles svc for this module.
- **`lead()`** — Handles lead for this module.
- **`employee()`** — Handles employee for this module.
- **`project()`** — Handles project for this module.
- **`task()`** — Handles task for this module.
- **`async test_create_task_commits(svc, lead, project, task)`** — Checks expected behavior for create task commits.
- **`async test_create_project_missing(svc, lead)`** — Checks expected behavior for create project missing.
- **`async test_create_denied_for_non_lead(svc, employee, project)`** — Checks error handling or rejection for create denied for non lead.
- **`async test_create_unallotted_employee(svc, lead, project)`** — Checks expected behavior for create unallotted employee.
- **`async test_list_project_tasks(svc, lead, project, task)`** — Checks expected behavior for list project tasks.
- **`async test_get_task_not_found(svc, lead)`** — Checks error handling or rejection for get task not found.
- **`async test_get_task_by_assigned_employee(svc, employee, project, task)`** — Checks expected behavior for get task by assigned employee.
- **`async test_get_task_denied_for_other_employee(svc, project, task)`** — Checks error handling or rejection for get task denied for other employee.
- **`async test_mine_excludes_inactive_memberships(svc, employee, task)`** — Checks expected behavior for mine excludes inactive memberships.
- **`async test_project_employee_tasks(svc, lead, project, task)`** — Checks expected behavior for project employee tasks.
- **`async test_project_employee_denied_for_other_employee(svc, employee, project)`** — Checks error handling or rejection for project employee denied for other employee.
- **`async test_update_task_commits(svc, lead, project, task)`** — Checks expected behavior for update task commits.
- **`async test_update_task_null_rejected(svc, lead, project, task)`** — Checks error handling or rejection for update task null rejected.
- **`async test_update_task_invalid_dates(svc, lead, project, task)`** — Checks error handling or rejection for update task invalid dates.
- **`async test_update_task_reassign(svc, lead, project, task)`** — Checks expected behavior for update task reassign.
- **`async test_progress_100_completes_task(svc, employee, task)`** — Checks expected behavior for progress 100 completes task.
- **`async test_progress_denied_to_other_employee(svc, task)`** — Checks error handling or rejection for progress denied to other employee.
- **`async test_progress_50_sets_in_progress(svc, employee, task)`** — Checks expected behavior for progress 50 sets in progress.
- **`async test_delete_task_commits(svc, lead, project, task)`** — Checks expected behavior for delete task commits.
- **`async test_delete_task_failure_rolls_back(svc, lead, project, task)`** — Checks error handling or rejection for delete task failure rolls back.

## Related project modules

Uses: `app.exceptions.auth_exception`, `app.exceptions.project_exception`, `app.exceptions.task_exception`, `app.schemas.task`, `app.services.task_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
