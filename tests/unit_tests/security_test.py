from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify():
    hashed = hash_password("Secret@123")
    assert hashed != "Secret@123"
    assert verify_password("Secret@123", hashed) is True
    assert verify_password("Wrong@123", hashed) is False


def test_token_round_trip():
    assert decode_access_token(create_access_token("user@test.com")) == "user@test.com"


def test_tampered_token_rejected():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(create_access_token("user@test.com") + "x")


def _token(**extra):
    s, now = get_settings(), datetime.now(UTC)
    claims = {"sub": "a@b.com", "iat": now, "exp": now + timedelta(minutes=5), "type": "access", **extra}
    return jwt.encode(claims, s.security_key, algorithm=s.algorithm)


def test_expired_token_rejected():
    past = datetime.now(UTC) - timedelta(hours=1)
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(_token(iat=past, exp=past + timedelta(minutes=1)))


def test_wrong_token_type_rejected():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(_token(type="refresh"))
