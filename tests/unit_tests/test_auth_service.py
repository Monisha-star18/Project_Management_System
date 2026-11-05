from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from jwt.exceptions import InvalidTokenError as JWTDecodeError

from app.exceptions.auth_exception import InvalidCredentialsError, InvalidTokenError, InactiveUserError
from app.services.auth_service import AuthService


@pytest.fixture
def svc():
    repo = AsyncMock()
    return AuthService(repo), repo


@pytest.fixture
def user():
    return SimpleNamespace(employee_id=101, email="ravi@test.com",
                           password_hash="stored-hash", is_active=True)


async def test_login_success(svc, user, monkeypatch):
    service, repo = svc
    repo.get_employee_by_email.return_value = user
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda password, hashed: True)
    monkeypatch.setattr("app.services.auth_service.create_access_token", lambda email: "fake-token")

    token = await service.login("ravi@test.com", "Passw0rd@1")

    assert token == "fake-token"
    repo.get_employee_by_email.assert_awaited_once_with("ravi@test.com")


async def test_login_user_not_found(svc):
    service, repo = svc
    repo.get_employee_by_email.return_value = None

    with pytest.raises(InvalidCredentialsError):
        await service.login("missing@test.com", "wrong")


async def test_login_wrong_password(svc, user, monkeypatch):
    service, repo = svc
    repo.get_employee_by_email.return_value = user
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda password, hashed: False)

    with pytest.raises(InvalidCredentialsError):
        await service.login("ravi@test.com", "wrong")


async def test_login_inactive_user(svc, user, monkeypatch):
    service, repo = svc
    user.is_active = False
    repo.get_employee_by_email.return_value = user
    monkeypatch.setattr("app.services.auth_service.verify_password", lambda password, hashed: True)

    with pytest.raises(InactiveUserError):
        await service.login("ravi@test.com", "Passw0rd@1")


async def test_get_me_success(svc, user, monkeypatch):
    service, repo = svc
    monkeypatch.setattr("app.services.auth_service.decode_access_token", lambda token: "ravi@test.com")
    repo.get_employee_by_email.return_value = user

    assert await service.get_me("valid-token") is user


async def test_get_me_invalid_token(svc, monkeypatch):
    service, _ = svc

    def invalid(token):
        raise JWTDecodeError("expired")

    monkeypatch.setattr("app.services.auth_service.decode_access_token", invalid)

    with pytest.raises(InvalidTokenError):
        await service.get_me("bad-token")


async def test_get_me_user_not_found(svc, monkeypatch):
    service, repo = svc
    monkeypatch.setattr("app.services.auth_service.decode_access_token", lambda token: "missing@test.com")
    repo.get_employee_by_email.return_value = None

    with pytest.raises(InvalidTokenError):
        await service.get_me("token")


async def test_get_me_inactive_user(svc, user, monkeypatch):
    service, repo = svc
    user.is_active = False
    monkeypatch.setattr("app.services.auth_service.decode_access_token", lambda token: "ravi@test.com")
    repo.get_employee_by_email.return_value = user

    with pytest.raises(InactiveUserError):
        await service.get_me("token")
