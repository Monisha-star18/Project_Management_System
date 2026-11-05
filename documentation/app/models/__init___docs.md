# __init__.py — File Documentation

**Original file:** `app/models/__init__.py`

## Main usage
Imports ORM model classes so metadata and database migrations can discover them.

## Why this file is needed
Model registration keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## What this file contains
Module-level definitions, imports, configuration, or database metadata rather than standalone functions.

## Related project modules

Uses: `app.models.employee`, `app.models.project`, `app.models.project_allotment`, `app.models.task`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
