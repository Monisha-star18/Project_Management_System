
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database.session import get_session
from app.models.user import UsersDetails
from app.exceptions.auth_exception import (
    InvalidCredentialsError,
    InactiveUserError,
    PermissionDeniedError
)
from app.repositories.interfaces.auth_repository_interface import (
    AuthRepositoryInterface
)
from app.repositories.implementation.auth_repository import (
    AuthRepository
)
from app.services.auth_service import AuthService


# Repository dependency
def get_auth_repository( db: AsyncSession = Depends(get_session) ) -> AuthRepositoryInterface:

    return AuthRepository(db)

# Service dependency
def get_auth_service( 
        repository: AuthRepositoryInterface = Depends(get_auth_repository)
        ) -> AuthService:

    return AuthService(repository)

# Extract bearer token
oauth2_scheme = OAuth2PasswordBearer( tokenUrl="/api/auth/login" )

# Authenticate current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service:AuthService=Depends(get_auth_service)
) -> UsersDetails:

    return await service.get_me(token)


# Authorize user by role
def require_roles(*allowed_roles: str):

    async def role_checker( 
            current_user: UsersDetails = Depends(get_current_user) 
    ) -> UsersDetails:

        if current_user.role not in allowed_roles:
            raise PermissionDeniedError()

        return current_user

    return role_checker
