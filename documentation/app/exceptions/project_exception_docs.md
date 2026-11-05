# project_exception.py — File Documentation

**Original file:** `app/exceptions/project_exception.py`

## Main usage
Defines meaningful application errors for project exception failures instead of generic exceptions.

## Why this file is needed
Domain-specific exceptions keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`ProjectNotFoundError`** — Custom error raised when project not found occurs.
- **`ProjectAlreadyExistsError`** — Custom error raised when project already exists occurs.
- **`InvalidProjectLeadError`** — Custom error raised when invalid project lead occurs.
- **`InvalidProjectUpdateError`** — Custom error raised when invalid project update occurs.
- **`InvalidProjectDurationError`** — Custom error raised when invalid project duration occurs.
- **`ProjectAccessDeniedError`** — Custom error raised when project access denied occurs.

## Functions / methods (short explanation)

- **`ProjectNotFoundError.__init__(self)`** — Stores dependencies or initializes an object.
- **`ProjectAlreadyExistsError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InvalidProjectLeadError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InvalidProjectUpdateError.__init__(self, message)`** — Stores dependencies or initializes an object.
- **`InvalidProjectDurationError.__init__(self)`** — Stores dependencies or initializes an object.
- **`ProjectAccessDeniedError.__init__(self)`** — Stores dependencies or initializes an object.

## Related project modules

Uses: `app.exceptions.base_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
