# triggers.sql — File Documentation

**Original file:** `db/triggers.sql`

## Main usage
Contains SQL statements used to implement database-side trigger behavior.

## Why this file is needed
Database trigger SQL keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Main contents

SQL statements define database-level behavior and are executed by PostgreSQL rather than called as Python functions.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
