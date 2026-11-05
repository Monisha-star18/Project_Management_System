# employee_created_email.py — File Documentation

**Original file:** `app/services/email/employee_created_email.py`

## Main usage
Builds notification content when an employee account is created.

## Why this file is needed
Employee welcome email keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`EmployeeCreatedEmail`** — Encapsulates the construction/delivery of this notification email.

## Functions / methods (short explanation)

- **`EmployeeCreatedEmail.build_message(self, full_name)`** — Builds the subject and body of the notification email.

## Related project modules

Uses: `app.services.email.base_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
