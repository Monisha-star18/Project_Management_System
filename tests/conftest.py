import os

# Fake settings for every test, so nothing touches your real .env, database or Mailjet.
# conftest.py loads before the test files, i.e. before any "app" module is imported.
os.environ.update(
    DB_NAME="test_db", DB_USER="test", DB_PASSWORD="test",
    ADMIN_USERNAME="admin", ADMIN_PASSWORD="admin-pass", ADMIN_EMAIL="admin@test.com", ADMIN_ROLE="admin",
    JWT_SECRET_KEY="test-secret-key-that-is-long-enough-32b", JWT_ALGORITHM="HS256", ACCESS_TOKEN_EXPIRE_MINUTES="30",
    MAILJET_API_KEY="key", MAILJET_SECRET_KEY="secret",
    MAILJET_SENDER_EMAIL="sender@test.com", MAILJET_SENDER_NAME="Admin",
)
