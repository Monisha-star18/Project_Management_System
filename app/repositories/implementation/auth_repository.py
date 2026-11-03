
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UsersDetails
from app.repositories.interfaces.auth_repository_interface import (
    AuthRepositoryInterface
)


class AuthRepository(AuthRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self,username: str ) -> UsersDetails | None:

        result = await self.db.execute(
            select(UsersDetails).where( UsersDetails.user_name == username)
        )

        return result.scalar_one_or_none()

    async def get_user_by_id( self, user_id: int) -> UsersDetails | None:

        result = await self.db.execute(
            select(UsersDetails).where( UsersDetails.user_id == user_id )
        )

        return result.scalar_one_or_none()
