# project_allotted_email.py — File Documentation

**Original file:** `app/services/email/project_allotted_email.py`

## Main usage
Builds notification content for employees added to a project.

## Why this file is needed
Project assignment email keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectAllottedEmail`** — Encapsulates the construction/delivery of this notification email.

## Functions / methods (short explanation)

- **`ProjectAllottedEmail.__init__(self, project_id, lead_name)`** — Stores dependencies or initializes an object.
- **`ProjectAllottedEmail.build_message(self, full_name)`** — Builds the subject and body of the notification email.

## Related project modules

Uses: `app.core.config`, `app.services.email.base_email`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
