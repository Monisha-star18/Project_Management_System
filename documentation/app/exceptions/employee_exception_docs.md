# employee_exception.py — File Documentation

**Original file:** `app/exceptions/employee_exception.py`

## Main usage
Defines meaningful application errors for employee exception failures instead of generic exceptions.

## Why this file is needed
Domain-specific exceptions keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`EmployeeAlreadyExistsError`** — Custom error raised when employee already exists occurs.
- **`EmployeeNotFoundError`** — Custom error raised when employee not found occurs.
- **`InvalidEmployeeUpdateError`** — Custom error raised when invalid employee update occurs.

## Functions / methods (short explanation)

- **`EmployeeAlreadyExistsError.__init__(self)`** — Stores dependencies or initializes an object.
- **`EmployeeNotFoundError.__init__(self)`** — Stores dependencies or initializes an object.
- **`InvalidEmployeeUpdateError.__init__(self)`** — Stores dependencies or initializes an object.

## Related project modules

Uses: `app.exceptions.base_exception`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
