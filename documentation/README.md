# Project Management System — Internal Documentation

This folder documents the application's source code **file by file**. Each document answers: **What is its main usage? Why is it needed? What do its classes and functions do?**

## Architecture

```text
Client / Swagger UI
      ↓
app/api/routers/          HTTP endpoints, request handling
      ↓
app/api/dependency/       FastAPI dependency injection
      ↓
app/services/             Business logic and permissions
      ↓
app/repositories/interfaces/       Repository contracts
      ↓
app/repositories/implementation/   Database access
      ↓
app/models/ + app/database/       SQLAlchemy / PostgreSQL
```

Cross-cutting modules: `app/core/` (settings/security), `app/schemas/` (validation), `app/exceptions/` (errors), `app/middleware/` (logging), `app/services/email/` (notifications), `alembic/` (database migrations), and `tests/` (verification).

## Common workflows

**Employee creation:** `employee.py` router → `employee_dependency.py` → `employee_service.py` → `employee_repository.py` → `employee.py` ORM model. Employee validation lives in `app/schemas/employee.py`.

**Task assignment:** `task.py` router → task service → task repository → task/allotment models. The service checks the project, authorized lead, and selected employee's project allotment.

**Login:** auth router → auth service → auth repository → employee model, with JWT/password helpers in `app/core/security.py`.

**Project reports:** report router → report service → report repository, where totals, completion percentage, and average progress are calculated.

## Folder guide

- `app/api/routers/`: API paths, HTTP methods, authentication dependencies, responses.
- `app/api/dependency/`: Object providers that connect routers, services, and repositories.
- `app/services/`: Business decisions, validation, permission enforcement, and transaction handling.
- `app/repositories/interfaces/`: Abstract method contracts for persistence.
- `app/repositories/implementation/`: Actual database queries and CRUD operations.
- `app/models/`: ORM tables and relationships.
- `app/schemas/`: Pydantic request/response formats.
- `app/core/`, `app/database/`: Shared configuration, security, and DB setup.
- `app/exceptions/`: Application-specific failures and error formatting.
- `alembic/`, `db/`: Schema migrations and SQL triggers.
- `tests/`: API tests, unit tests, and fixtures.

## File-by-file documentation index

- [`.env.example`](.env_docs.md) — Environment template
- [`.gitignore`](.gitignore_docs.md) — Git ignore rules
- [`README.md`](README_docs.md) — Project README
- [`alembic/README`](alembic/README_docs.md) — Migration README
- [`alembic/env.py`](alembic/env_docs.md) — Migration environment
- [`alembic/script.py.mako`](alembic/script.py_docs.md) — Migration template
- [`alembic/versions/7c2263fd67e9_create_the_orm_tables.py`](alembic/versions/7c2263fd67e9_create_the_orm_tables_docs.md) — Initial table migration
- [`alembic/versions/eb832bb33e83_auto_allotment_project_lead_trigger.py`](alembic/versions/eb832bb33e83_auto_allotment_project_lead_trigger_docs.md) — Project-lead allotment migration
- [`alembic.ini`](alembic_docs.md) — Alembic configuration
- [`app/api/dependency/auth.py`](app/api/dependency/auth_docs.md) — Dependency injection
- [`app/api/dependency/employee_dependency.py`](app/api/dependency/employee_dependency_docs.md) — Dependency injection
- [`app/api/dependency/project_allotment_dependency.py`](app/api/dependency/project_allotment_dependency_docs.md) — Dependency injection
- [`app/api/dependency/project_dependency.py`](app/api/dependency/project_dependency_docs.md) — Dependency injection
- [`app/api/dependency/report_dependency.py`](app/api/dependency/report_dependency_docs.md) — Dependency injection
- [`app/api/dependency/task_dependency.py`](app/api/dependency/task_dependency_docs.md) — Dependency injection
- [`app/api/routers/auth.py`](app/api/routers/auth_docs.md) — Authentication endpoints
- [`app/api/routers/employee.py`](app/api/routers/employee_docs.md) — Employee endpoints
- [`app/api/routers/health.py`](app/api/routers/health_docs.md) — Health endpoints
- [`app/api/routers/project.py`](app/api/routers/project_docs.md) — Project endpoints
- [`app/api/routers/project_allotment.py`](app/api/routers/project_allotment_docs.md) — Project membership endpoints
- [`app/api/routers/report.py`](app/api/routers/report_docs.md) — Project reports endpoint
- [`app/api/routers/task.py`](app/api/routers/task_docs.md) — Task endpoints
- [`app/core/config.py`](app/core/config_docs.md) — Configuration management
- [`app/core/security.py`](app/core/security_docs.md) — Authentication utilities
- [`app/database/base.py`](app/database/base_docs.md) — ORM base
- [`app/database/connection.py`](app/database/connection_docs.md) — Database engine
- [`app/database/session.py`](app/database/session_docs.md) — Database session dependency
- [`app/exceptions/auth_exception.py`](app/exceptions/auth_exception_docs.md) — Domain-specific exceptions
- [`app/exceptions/base_exception.py`](app/exceptions/base_exception_docs.md) — Application error base
- [`app/exceptions/employee_exception.py`](app/exceptions/employee_exception_docs.md) — Domain-specific exceptions
- [`app/exceptions/handlers.py`](app/exceptions/handlers_docs.md) — Exception-to-HTTP conversion
- [`app/exceptions/project_allotment_exception.py`](app/exceptions/project_allotment_exception_docs.md) — Domain-specific exceptions
- [`app/exceptions/project_exception.py`](app/exceptions/project_exception_docs.md) — Domain-specific exceptions
- [`app/exceptions/task_exception.py`](app/exceptions/task_exception_docs.md) — Domain-specific exceptions
- [`app/main.py`](app/main_docs.md) — Application entry point
- [`app/middleware/logging_middleware.py`](app/middleware/logging_middleware_docs.md) — HTTP logging middleware
- [`app/models/__init__.py`](app/models/__init___docs.md) — Model registration
- [`app/models/employee.py`](app/models/employee_docs.md) — ORM database model
- [`app/models/project.py`](app/models/project_docs.md) — ORM database model
- [`app/models/project_allotment.py`](app/models/project_allotment_docs.md) — ORM database model
- [`app/models/task.py`](app/models/task_docs.md) — ORM database model
- [`app/repositories/implementation/auth_repository.py`](app/repositories/implementation/auth_repository_docs.md) — Database repository
- [`app/repositories/implementation/employee_repository.py`](app/repositories/implementation/employee_repository_docs.md) — Database repository
- [`app/repositories/implementation/project_allotment_repository.py`](app/repositories/implementation/project_allotment_repository_docs.md) — Database repository
- [`app/repositories/implementation/project_repository.py`](app/repositories/implementation/project_repository_docs.md) — Database repository
- [`app/repositories/implementation/report_repository.py`](app/repositories/implementation/report_repository_docs.md) — Database repository
- [`app/repositories/implementation/task_repository.py`](app/repositories/implementation/task_repository_docs.md) — Database repository
- [`app/repositories/interfaces/auth_repository_interface.py`](app/repositories/interfaces/auth_repository_interface_docs.md) — Repository contract
- [`app/repositories/interfaces/employee_repository_interface.py`](app/repositories/interfaces/employee_repository_interface_docs.md) — Repository contract
- [`app/repositories/interfaces/project_allotment_repository_interface.py`](app/repositories/interfaces/project_allotment_repository_interface_docs.md) — Repository contract
- [`app/repositories/interfaces/project_repository_interface.py`](app/repositories/interfaces/project_repository_interface_docs.md) — Repository contract
- [`app/repositories/interfaces/report_repository_interface.py`](app/repositories/interfaces/report_repository_interface_docs.md) — Repository contract
- [`app/repositories/interfaces/task_repository_interface.py`](app/repositories/interfaces/task_repository_interface_docs.md) — Repository contract
- [`app/schemas/auth.py`](app/schemas/auth_docs.md) — API data schema
- [`app/schemas/employee.py`](app/schemas/employee_docs.md) — API data schema
- [`app/schemas/project.py`](app/schemas/project_docs.md) — API data schema
- [`app/schemas/project_allotment.py`](app/schemas/project_allotment_docs.md) — API data schema
- [`app/schemas/report.py`](app/schemas/report_docs.md) — API data schema
- [`app/schemas/task.py`](app/schemas/task_docs.md) — API data schema
- [`app/scripts/create_admin.py`](app/scripts/create_admin_docs.md) — Admin initialization
- [`app/services/auth_service.py`](app/services/auth_service_docs.md) — Authentication business logic
- [`app/services/email/base_email.py`](app/services/email/base_email_docs.md) — Email transport
- [`app/services/email/employee_created_email.py`](app/services/email/employee_created_email_docs.md) — Employee welcome email
- [`app/services/email/project_allotted_email.py`](app/services/email/project_allotted_email_docs.md) — Project assignment email
- [`app/services/email/task_assigned_email.py`](app/services/email/task_assigned_email_docs.md) — Task assignment email
- [`app/services/employee_service.py`](app/services/employee_service_docs.md) — Employee business logic
- [`app/services/project_allotment_service.py`](app/services/project_allotment_service_docs.md) — Project membership business logic
- [`app/services/project_service.py`](app/services/project_service_docs.md) — Project business logic
- [`app/services/report_service.py`](app/services/report_service_docs.md) — Project reporting business logic
- [`app/services/task_service.py`](app/services/task_service_docs.md) — Task business logic
- [`app/utilites/logger.py`](app/utilites/logger_docs.md) — Application logging
- [`db/triggers.sql`](db/triggers_docs.md) — Database trigger SQL
- [`pytest.ini`](pytest_docs.md) — Pytest configuration
- [`requirements.txt`](requirements_docs.md) — Python dependencies
- [`tests/api/test_auth_api.py`](tests/api/test_auth_api_docs.md) — API integration tests
- [`tests/api/test_employee_api.py`](tests/api/test_employee_api_docs.md) — API integration tests
- [`tests/api/test_health_api.py`](tests/api/test_health_api_docs.md) — API integration tests
- [`tests/api/test_project_allotment_api.py`](tests/api/test_project_allotment_api_docs.md) — API integration tests
- [`tests/api/test_project_api.py`](tests/api/test_project_api_docs.md) — API integration tests
- [`tests/api/test_report_api.py`](tests/api/test_report_api_docs.md) — API integration tests
- [`tests/api/test_task_api.py`](tests/api/test_task_api_docs.md) — API integration tests
- [`tests/conftest.py`](tests/conftest_docs.md) — Shared test fixtures
- [`tests/unit_tests/employee_service_test.py`](tests/unit_tests/employee_service_test_docs.md) — Unit tests
- [`tests/unit_tests/security_test.py`](tests/unit_tests/security_test_docs.md) — Unit tests
- [`tests/unit_tests/test_auth_service.py`](tests/unit_tests/test_auth_service_docs.md) — Unit tests
- [`tests/unit_tests/test_project_allotment_service.py`](tests/unit_tests/test_project_allotment_service_docs.md) — Unit tests
- [`tests/unit_tests/test_project_service.py`](tests/unit_tests/test_project_service_docs.md) — Unit tests
- [`tests/unit_tests/test_task_service.py`](tests/unit_tests/test_task_service_docs.md) — Unit tests

## Documentation scope

- Generated for the project's Python source files, tests, migrations, and selected human-maintained configuration files.
- Third-party `.venv/` packages, Git internals, caches, generated logs, and real `.env` secrets are deliberately excluded from the documented distribution.
- The original application source logic was not changed. Create your own `.env` using `.env.example` before running the project.
