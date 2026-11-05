from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

setting = get_settings()

password_hasher = PasswordHash.recommended()

SECRET_KEY = setting.security_key
EXPIRE_MINUTES = setting.expire_time
ALGORITHM = setting.algorithm


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, 
                    hashed_password: str) -> bool:
    
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(email_id: str) -> str:
    settings = get_settings()

    now = datetime.now(UTC)

    payload = {
        "sub": str(email_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.expire_time),
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.security_key,
        algorithm=settings.algorithm
    )


def decode_access_token(token: str) -> int:
    settings = get_settings()

    payload = jwt.decode(
        token,
        settings.security_key,
        algorithms=[settings.algorithm],
        options={
            "require": ["sub", "iat", "exp"]
        }
    )

    if payload.get("type") != "access":
        raise jwt.InvalidTokenError(
            "Invalid token type"
        )

    subject = payload["sub"]

    email_id = subject


    return email_id
