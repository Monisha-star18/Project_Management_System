# task_exception.py — File Documentation

**Original file:** `app/exceptions/task_exception.py`

## Main usage
Defines meaningful application errors for task exception failures instead of generic exceptions.

## Why this file is needed
Domain-specific exceptions keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`TaskNotFoundError`** — Custom error raised when task not found occurs.
- **`TaskAssignmentError`** — Custom error raised when task assignment occurs.
- **`InvalidTaskUpdateError`** — Custom error raised when invalid task update occurs.
- **`TaskProjectAccessDeniedError`** — Custom error raised when task project access denied occurs.

## Functions / methods (short explanation)

- **`TaskNotFoundError.__init__(self)`** — Stores dependencies or initializes an object.
- **`TaskAssignmentError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InvalidTaskUpdateError.__init__(self, message)`** — Stores dependencies or initializes an object.
- **`TaskProjectAccessDeniedError.__init__(self)`** — Stores dependencies or initializes an object.

## Related project modules

Uses: `app.exceptions.base_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
