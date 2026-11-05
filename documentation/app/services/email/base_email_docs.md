# base_email.py — File Documentation

**Original file:** `app/services/email/base_email.py`

## Main usage
Builds and sends email messages through the configured provider.

## Why this file is needed
Email transport keeps this responsibility in one place. This separation makes the code easier to maintain, test, and reuse without mixing it into unrelated parts of the application.

## Classes / models

- **`BaseEmail`** — Encapsulates the construction/delivery of this notification email.

## Functions / methods (short explanation)

- **`BaseEmail.__init__(self, sender_email)`** — Stores dependencies or initializes an object.
- **`BaseEmail.build_message(self, full_name)`** — Builds the subject and body of the notification email.
- **`async BaseEmail.send(self, email, full_name)`** — Sends the composed email through the configured email provider.

## Related project modules

Uses: `app.core.config`, `app.utilites.logger`.

## Notes
- Explanations are based on the uploaded source code.
- This documentation describes existing behavior; it does not modify the application logic.
