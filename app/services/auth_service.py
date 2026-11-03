
from jwt.exceptions import InvalidTokenError as JWTDecodeError

from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password
)
from app.exceptions.auth_exception import (
    InvalidCredentialsError,
    InvalidTokenError,
    InactiveUserError
)
from app.models.employee import EmployeeData
from app.repositories.interfaces.auth_repository_interface import (
    AuthRepositoryInterface
)
from app.utilites.logger import logger


class AuthService:

    def __init__( self, repository: AuthRepositoryInterface ):
        self.repository = repository

    async def login( self, email_id: str, password: str ) -> str:

        user = await self.repository.get_employee_by_email(email_id)

        if user is None:
            logger.warning("Login failed")
            raise InvalidCredentialsError()

        if not verify_password( password, user.password_hash):
            logger.warning("Login failed")
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError()

        access_token = create_access_token( user.email )

        logger.info(
            "Login successful | UserID=%s",
            user.employee_id
        )

        return access_token

    async def get_me( self, token: str) -> EmployeeData:

        try:
            email_id = decode_access_token(token)

        except JWTDecodeError as exc:
            raise InvalidTokenError() from exc

        user = await self.repository.get_employee_by_email(email_id)

        if user is None:
            raise InvalidTokenError()

        if not user.is_active:
            raise InactiveUserError()

        return user

    async def register_new_user(self):
        pass