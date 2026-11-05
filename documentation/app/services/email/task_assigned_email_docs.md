# task_assigned_email.py — File Documentation

**Original file:** `app/services/email/task_assigned_email.py`

## Main usage
Builds notification content when a task is assigned.

## Why this file is needed
Task assignment email keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskAssignedEmail`** — Encapsulates the construction/delivery of this notification email.

## Functions / methods (short explanation)

- **`TaskAssignedEmail.__init__(self, project_id, task_title, priority, start_date, due_date, lead_name)`** — Stores dependencies or initializes an object.
- **`TaskAssignedEmail.build_message(self, full_name)`** — Builds the subject and body of the notification email.

## Related project modules

Uses: `app.core.config`, `app.services.email.base_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
