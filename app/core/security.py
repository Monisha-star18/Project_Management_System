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


def create_access_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])