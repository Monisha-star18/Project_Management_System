import os

import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.database.base import Base
from app.database.session import get_session
from app.main import app

from datetime import date

from app.models.employee import EmployeeData
from app.core.security import hash_password, create_access_token


# Fake settings for every test, so nothing touches your real .env, database or Mailjet.
# conftest.py loads before the test files, i.e. before any "app" module is imported.
os.environ.update(
    DB_NAME="test_db", DB_USER="test", DB_PASSWORD="test",
    ADMIN_USERNAME="admin", ADMIN_PASSWORD="admin-pass", ADMIN_EMAIL="admin@test.com", ADMIN_ROLE="admin",
    JWT_SECRET_KEY="test-secret-key-that-is-long-enough-32b", JWT_ALGORITHM="HS256", ACCESS_TOKEN_EXPIRE_MINUTES="30",
    MAILJET_API_KEY="key", MAILJET_SECRET_KEY="secret",
    MAILJET_SENDER_EMAIL="sender@test.com", MAILJET_SENDER_NAME="Admin",
)



settings = get_settings()


# Prevent using development database
if settings.test_db_name == settings.db_name:
    raise RuntimeError(
        "Test database cannot be the development database"
    )


# Create test database engine
@pytest_asyncio.fixture
async def test_engine():

    engine = create_async_engine(
        settings.test_database_url,
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


# Create test database session
@pytest_asyncio.fixture
async def test_session(test_engine):

    TestingSessionLocal = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False
    )

    async with TestingSessionLocal() as session:
        yield session


# Override dependency and create HTTP client
@pytest_asyncio.fixture
async def client(test_session):

    async def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.pop(get_session, None)

@pytest_asyncio.fixture
async def admin(test_session):

    admin = EmployeeData(
        full_name="Test Admin",
        email="admin@test.com",
        phone="9876543210",
        department="IT",
        role="admin",
        password_hash=hash_password("Admin@123"),
        joining_date=date(2026, 1, 1),
        is_active=True
    )

    test_session.add(admin)
    await test_session.commit()
    await test_session.refresh(admin)

    return admin


@pytest_asyncio.fixture
async def auth_headers(admin):

    token = create_access_token(admin.email)

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest_asyncio.fixture
async def team_lead(test_session):

    lead = EmployeeData(
        full_name="Test Team Lead",
        email="lead@test.com",
        phone="9876543211",
        department="IT",
        role="team_lead",
        password_hash=hash_password("Lead@123"),
        joining_date=date(2026, 1, 1),
        is_active=True,
    )

    test_session.add(lead)
    await test_session.commit()
    await test_session.refresh(lead)

    return lead


@pytest_asyncio.fixture
async def lead_headers(team_lead):

    token = create_access_token(team_lead.email)

    return {
        "Authorization": f"Bearer {token}"
    }
