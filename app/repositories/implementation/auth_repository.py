
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import EmployeeData
from app.repositories.interfaces.auth_repository_interface import (
    AuthRepositoryInterface
)


class AuthRepository(AuthRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_employee_by_email( self, email_id:str) -> EmployeeData | None:

        result = await self.db.execute(
            select(EmployeeData).where( EmployeeData.email == email_id )
        )

        return result.scalar_one_or_none()
