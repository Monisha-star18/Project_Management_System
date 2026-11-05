# Project Management System API

An asynchronous, role-based backend application for managing employees, projects, team assignments, tasks, and project progress through REST APIs.

## 1. Project Abstract

The **Project Management System** is a REST API designed to organize project work within an organization. Administrators can manage employees and projects, assign a team lead to each project, and review project information. Team leads can manage project allotments and assign tasks to employees. Employees can view their assigned tasks and update task progress.

The system provides a project report showing project details, the number of actively allotted employees, total tasks, completed tasks, and the completion percentage. JWT authentication and role-based authorization control access to protected endpoints. The backend uses **FastAPI**, **async SQLAlchemy**, **PostgreSQL**, and a layered architecture with API routers, dependency providers, Pydantic schemas, services, repository interfaces, and repository implementations. Unit and API tests are included.

## 2. Main Features

- JWT-based login and authenticated user profile retrieval.
- Role-based access control for **admin**, **team_lead**, and **employee**.
- Employee registration, retrieval, paginated listing, updates, and soft deletion.
- Project creation, listing, retrieval, updates, team-lead changes, and deletion.
- Project allotment: add employees, list project members, view an employee's allotments, and remove an employee from a project.
- Automatic project-lead allotment through a PostgreSQL trigger migration.
- Task creation, assignment, retrieval, updates, progress tracking, and deletion.
- Employee-specific task views and project-specific task lists.
- Project reports with employee counts, task counts, completed task counts, and completion percentages.
- Employee welcome-email functionality using Mailjet.
- Health and database connectivity endpoints, HTTP request logging, and custom exception handling.
- Unit tests for services/security and integration-style API tests with a separate PostgreSQL test database.

## 3. Technology Stack and Concepts

| Technology / Concept | Purpose |
|---|---|
| Python | Backend programming language. |
| FastAPI | Async REST APIs, dependency injection, and OpenAPI documentation. |
| Pydantic / Pydantic Settings | Request/response validation and `.env` configuration. |
| PostgreSQL | Relational database for employees, projects, allotments, and tasks. |
| SQLAlchemy Async ORM | Database models, relationships, and asynchronous sessions. |
| asyncpg | Async PostgreSQL driver. |
| Alembic | Version-controlled database migrations, including the allotment trigger. |
| PyJWT | Signed access-token creation and verification. |
| Argon2 via `pwdlib` | Password hashing and verification. |
| Role-Based Access Control (RBAC) | Limits API access by user role. |
| Repository Interfaces | Abstract contracts for data-access implementations. |
| Service Layer | Business rules, validations, and coordination of operations. |
| Dependency Injection | Provides database sessions, repositories, and services to routers. |
| SQLAlchemy `selectinload` | Eager loading of relationships for project reports and other queries. |
| HTTPX | Async HTTP client, including API tests and email-service requests. |
| pytest / pytest-asyncio | Service unit tests and asynchronous API tests. |
| Ruff | Python linting and formatting tool. |
| python-multipart | Form-data handling for login. |

## 4. Database Design

The application defines **four main tables** in `app/models/`:

| Table | Purpose |
|---|---|
| `employee` | Stores employee identity, contact details, department, role, password hash, join date, and active status. |
| `projects` | Stores project title, description, team lead, start/end dates, status, creator, and timestamps. |
| `project_allotments` | Links employees to projects; includes allotment timestamps, active status, and removal remarks. |
| `tasks` | Stores tasks associated with project allotments, including title, assignee context, assigning lead, priority, dates, status, progress, and remarks. |

### Main relationships

- One employee can **create multiple projects** as an administrator.
- One employee can **lead multiple projects** as a team lead.
- One project can have **multiple employee allotments**.
- One employee can have **multiple project allotments**.
- One allotment can have **multiple tasks**.
- Each task links to an allotment and records the employee who assigned it.

SQLAlchemy relationships and foreign keys enforce the links among these records. The models also define uniqueness, date, status, priority, and progress constraints.

**Project/task statuses:** Projects support `planning`, `started`, `pending`, `completed`, and `dropped`. Tasks support `todo`, `in_progress`, `completed`, and `on_hold`; progress is constrained to **0–100%**.

The project-lead auto-allotment database trigger is included in an Alembic revision under `alembic/versions/`.

## 5. Project Folder Structure

```text
Project_Management_System/
│
├── alembic/
│   ├── versions/                    # Database migration revisions
│   └── env.py                       # Alembic environment
├── alembic.ini
│
├── app/
│   ├── api/
│   │   ├── dependency/              # Authentication and service dependencies
│   │   └── routers/                 # Auth, employee, project, allotment, task, report, health
│   ├── core/                        # Settings and JWT/password utilities
│   ├── database/                    # Base, engine, and session configuration
│   ├── exceptions/                  # Application exceptions and handlers
│   ├── middleware/                   # Request logging middleware
│   ├── models/                       # SQLAlchemy models (4 main tables)
│   ├── repositories/
│   │   ├── interfaces/              # Repository contracts
│   │   └── implementation/          # Repository implementations
│   ├── schemas/                      # Pydantic request/response models
│   ├── scripts/                      # Initial admin creation
│   ├── services/                     # Business logic and email service
│   │   └── email/
│   ├── utilites/                     # Application logger (directory name as in source)
│   └── main.py                       # FastAPI app and router registration
│
├── db/
│   └── triggers.sql                  # SQL trigger scripts
├── tests/
│   ├── api/                          # API tests
│   ├── unit_tests/                   # Service and security unit tests
│   └── conftest.py                  # Test fixtures and test DB override
│
├── .env.example                      # Example environment variables
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## 6. Environment Configuration

Create a **`.env`** file in the project root. Use the existing `.env.example` as a starting point, and provide your own values. **Never commit real passwords, JWT secrets, or Mailjet credentials.**

| Variable | Description |
|---|---|
| `APP_NAME` | Application name; optional, with a default in settings. |
| `DB_HOST` | PostgreSQL hostname, e.g. `localhost`. |
| `DB_PORT` | PostgreSQL port, usually `5432`. |
| `DB_NAME` | Main application database name. |
| `DB_USER` | PostgreSQL username. |
| `DB_PASSWORD` | PostgreSQL password. |
| `TEST_DB_NAME` | Separate PostgreSQL database used for automated API tests. |
| `ADMIN_USERNAME` | Name for the initial administrator. |
| `ADMIN_EMAIL` | Email for the initial administrator. |
| `ADMIN_PASSWORD` | Password for the initial administrator. |
| `ADMIN_ROLE` | Initial admin role configuration (`admin`). |
| `JWT_SECRET_KEY` | Secret used to sign JWTs. |
| `JWT_ALGORITHM` | JWT algorithm, e.g. `HS256`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime. |
| `MAILJET_API_KEY` | Mailjet API key. |
| `MAILJET_SECRET_KEY` | Mailjet secret key. |
| `MAILJET_SENDER_EMAIL` | Verified sending address. |
| `MAILJET_SENDER_NAME` | Sender display name. |

**Note:** The uploaded `.env.example` does not include `TEST_DB_NAME`, but `app/core/config.py` requires it. Add a line such as `TEST_DB_NAME=project_management_test` to your local `.env` (and to `.env.example` if you maintain the example).

The database URLs are built with SQLAlchemy `URL.create()` using the shared host, port, username, and password, and the appropriate database name. Passwords with URL-special characters do **not** need manual encoding with `quote_plus()`.

Create both PostgreSQL databases before running the application/tests, for example from PostgreSQL's query tool:

```sql
CREATE DATABASE project_management;
CREATE DATABASE project_management_test;
```

Use different names for development and test databases. The test fixtures **create and drop tables**, so never point tests at a database containing important data.

## 7. Installation and Running the Application

Run commands from the project root.

### 7.1 Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 7.2 Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 7.3 Configure your environment

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
cp .env.example .env
```

Edit `.env` with your database, test database, JWT, admin, and Mailjet settings. Remember to add `TEST_DB_NAME`.

### 7.4 Apply database migrations

```bash
alembic upgrade head
```

The migration history includes the initial tables and the automatic project-lead allotment trigger.

### 7.5 Start the API

```bash
uvicorn app.main:app --reload
```

By default, the API runs at `http://127.0.0.1:8000`.

The application lifespan also calls `create_admin()` on startup; make sure migrations have been applied and the initial administrator configuration is valid before launching.

## 8. API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **OpenAPI JSON:** `http://127.0.0.1:8000/openapi.json`
- **Application health:** `GET /api/health/`
- **Database health:** `GET /api/health/db`

### Authentication and employee endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/login` | Log in and receive a JWT access token. |
| GET | `/api/auth/me` | Get the authenticated user's details. |
| POST | `/api/employees/registration` | Create an employee (admin). |
| GET | `/api/employees/` | List employees with pagination. |
| GET | `/api/employees/{employee_id}` | Get an employee. |
| PATCH | `/api/employees/{employee_id}` | Update employee details (admin). |
| DELETE | `/api/employees/{employee_id}` | Soft-delete an employee (admin). |

Login uses **form data** with `username` (the user's email) and `password` via `OAuth2PasswordRequestForm`.

### Project and allotment endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/projects/` | Create a project (admin). |
| GET | `/api/projects/` | List projects. |
| GET | `/api/projects/{project_id}` | Get project details. |
| PATCH | `/api/projects/{project_id}` | Update a project (admin/team lead, subject to service checks). |
| PATCH | `/api/projects/{project_id}/lead` | Change the team lead (admin). |
| DELETE | `/api/projects/{project_id}` | Delete a project (admin). |
| POST | `/api/projects/{project_id}/allotments` | Allot an employee to a project (team lead). |
| GET | `/api/projects/{project_id}/allotments` | List employees allotted to a project. |
| GET | `/api/projects/employees/{employee_id}/allotments` | List an employee's project allotments. |
| DELETE | `/api/projects/{project_id}/allotments/{employee_id}` | Remove an employee from a project (team lead). |

### Task and report endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/projects/{project_id}/tasks` | Create and assign a task (team lead). |
| GET | `/api/projects/{project_id}/tasks` | List tasks in a project (admin/team lead). |
| GET | `/api/tasks/{task_id}` | Get task details (authorized user). |
| GET | `/api/employees/me/tasks` | View the current employee's tasks. |
| GET | `/api/projects/{project_id}/employees/{employee_id}/tasks` | View an employee's tasks within a project. |
| PATCH | `/api/tasks/{task_id}` | Update a task (team lead). |
| PATCH | `/api/tasks/{task_id}/progress` | Update assigned task progress (employee). |
| DELETE | `/api/tasks/{task_id}` | Delete a task (team lead). |
| GET | `/api/reports/projects/{project_id}` | Get a project progress report (admin/team lead). |

The **report** includes project details, active project-allotment count, total task count, completed task count, and a calculated completion percentage:

```text
completion_percentage = (completed_tasks / total_tasks) * 100
```

If the project has no tasks, the percentage is `0.0`. The repository eagerly loads the project's allotments and tasks with `selectinload()`; the service calculates the report values.

**Current implementation note:** The uploaded Auth router provides login and `/me`; it does **not** yet expose a refresh-token endpoint.

## 9. Running Tests with Pytest

The project includes service/security unit tests and API tests. API tests use **HTTPX `AsyncClient` + `ASGITransport`**, async pytest fixtures, and a separate PostgreSQL test database. `tests/conftest.py` overrides FastAPI's `get_session` dependency so test API requests use the test database.

Ensure `TEST_DB_NAME` is configured and the test database exists before running API tests. API test fixtures recreate tables, so use a disposable test database only.

### Run all tests

```bash
python -m pytest -v
```

### Run API tests

```bash
python -m pytest tests/api/ -v
```

### Run service and security unit tests

```bash
python -m pytest tests/unit_tests/ -v
```

### Run one feature's API tests

```bash
python -m pytest tests/api/test_employee_api.py -v
python -m pytest tests/api/test_project_api.py -v
python -m pytest tests/api/test_project_allotment_api.py -v
python -m pytest tests/api/test_task_api.py -v
python -m pytest tests/api/test_auth_api.py -v
python -m pytest tests/api/test_report_api.py -v
```

### Run one test function

```bash
python -m pytest tests/api/test_report_api.py::test_get_project_report_valid -v
```

### Show output and failure details

```bash
python -m pytest tests/api/ -v -s
python -m pytest -ra
```

These commands describe how to run the suite; they do not imply that every test has been verified as passing in this package.

## 10. Database Migrations with Alembic

The project includes Alembic migration files for ORM tables and a PostgreSQL trigger that automatically allots a newly created project's team lead.

**Apply migrations:**

```bash
alembic upgrade head
```

**Create a migration after modifying models:**

```bash
alembic revision --autogenerate -m "describe your change"
```

Review autogenerated migration files before applying them.

**Check the current revision and history:**

```bash
alembic current
alembic history
```

**Downgrade one revision (use with caution):**

```bash
alembic downgrade -1
```

Back up important data before any schema changes or downgrade.

## 11. Code Quality with Ruff

Ruff is included in `requirements.txt` for code-quality checks and formatting.

```bash
ruff check .
ruff check . --fix
ruff format .
ruff format . --check
```

Review automatic fixes and formatting changes before committing them.

## 12. Email Notification Notes

The employee-registration endpoint schedules a background email task using `EmployeeCreatedEmail` and the Mailjet service configuration. The email includes the new employee's name and address.

Make sure `MAILJET_API_KEY`, `MAILJET_SECRET_KEY`, `MAILJET_SENDER_EMAIL`, and `MAILJET_SENDER_NAME` are configured. Sender addresses may need verification with the email provider. Keep API credentials out of source control.

## 13. Logging and Error Handling

- `app/middleware/logging_middleware.py` logs HTTP method, path, response status, and request duration.
- `app/utilites/logger.py` configures the `project_management` logger.
- Application logs are written to `logs/app.log` with rotating log files.
- Domain-specific exceptions live in `app/exceptions/` and are handled using a shared FastAPI exception handler.
- Request and response validation is handled by Pydantic/FastAPI.

## 14. Important Notes

- Do not commit your real `.env`, database passwords, Mailjet keys, or JWT secret.
- Set **`TEST_DB_NAME`**, which is required by `Settings` but missing from the uploaded `.env.example`.
- Use a separate disposable PostgreSQL database for API tests; table setup/teardown can delete test-database tables.
- Run `alembic upgrade head` before starting the app against a new database.
- The administrator bootstrap runs during application startup and uses the application's normal database connection.
- Protect report and task endpoints according to the role requirements configured in their routers and services.
- The project report counts active allotments and tasks linked through allotments. Removing an allotment may also remove its tasks based on the configured deletion behavior.
- A refresh-token endpoint is **not implemented in the uploaded code**; add it only if you decide to extend authentication.
