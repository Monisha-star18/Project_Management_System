# project_allotment_exception.py — File Documentation

**Original file:** `app/exceptions/project_allotment_exception.py`

## Main usage
Defines meaningful application errors for project allotment exception failures instead of generic exceptions.

## Why this file is needed
Domain-specific exceptions keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`AllotmentNotFoundError`** — Custom error raised when allotment not found occurs.
- **`AllotmentConflictError`** — Custom error raised when allotment conflict occurs.
- **`InvalidAllotmentEmployeeError`** — Custom error raised when invalid allotment employee occurs.
- **`ProjectAllotmentNotFoundError`** — Custom error raised when project allotment not found occurs.
- **`ProjectAllotmentAccessDeniedError`** — Custom error raised when project allotment access denied occurs.

## Functions / methods (short explanation)

- **`AllotmentNotFoundError.__init__(self)`** — Stores dependencies or initializes an object.
- **`AllotmentConflictError.__init__(self, message)`** — Stores dependencies or initializes an object.
- **`InvalidAllotmentEmployeeError.__init__(self)`** — Stores dependencies or initializes an object.
- **`ProjectAllotmentNotFoundError.__init__(self)`** — Stores dependencies or initializes an object.
- **`ProjectAllotmentAccessDeniedError.__init__(self)`** — Stores dependencies or initializes an object.

## Related project modules

Uses: `app.exceptions.base_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
