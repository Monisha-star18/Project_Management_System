# test_project_allotment_service.py — File Documentation

**Original file:** `tests/unit_tests/test_project_allotment_service.py`

## Main usage
Checks individual functions and edge cases in project allotment service.

## Why this file is needed
Unit tests keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Functions / methods (short explanation)

- **`svc()`** — Handles svc for this module.
- **`employee()`** — Handles employee for this module.
- **`membership(employee)`** — Handles membership for this module.
- **`async test_add_employee_commits(svc, employee, membership)`** — Checks expected behavior for add employee commits.
- **`async test_add_employee_project_not_found(svc, employee)`** — Checks error handling or rejection for add employee project not found.
- **`async test_add_inactive_employee_rejected(svc, employee)`** — Checks error handling or rejection for add inactive employee rejected.
- **`async test_add_duplicate_membership(svc, employee, membership)`** — Checks error handling or rejection for add duplicate membership.
- **`async test_add_database_error_rolls_back(svc, employee)`** — Checks error handling or rejection for add database error rolls back.
- **`async test_list_members_excludes_inactive(svc, membership)`** — Checks expected behavior for list members excludes inactive.
- **`async test_list_members_project_not_found(svc)`** — Checks error handling or rejection for list members project not found.
- **`async test_remove_employee_commits(svc, employee, membership)`** — Checks expected behavior for remove employee commits.
- **`async test_remove_project_lead_rejected(svc, employee)`** — Checks error handling or rejection for remove project lead rejected.
- **`async test_remove_membership_not_found(svc, employee)`** — Checks error handling or rejection for remove membership not found.
- **`async test_remove_failure_rolls_back(svc, employee, membership)`** — Checks error handling or rejection for remove failure rolls back.
- **`async test_get_employee_allotments(svc, employee, membership)`** — Checks expected behavior for get employee allotments.
- **`async test_get_allotments_employee_not_found(svc)`** — Checks error handling or rejection for get allotments employee not found.

## Related project modules

Uses: `app.exceptions.employee_exception`, `app.exceptions.project_allotment_exception`, `app.schemas.project_allotment`, `app.services.project_allotment_service`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
