# base_exception.py — File Documentation

**Original file:** `app/exceptions/base_exception.py`

## Main usage
Defines the common parent error for expected business failures.

## Why this file is needed
Application error base keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`AppException`** — Custom error raised when app exception occurs.

## Functions / methods (short explanation)

- **`AppException.__init__(self, message, status_code)`** — Stores dependencies or initializes an object.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
