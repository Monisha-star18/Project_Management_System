
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.employee_exception import EmployeeAlreadyExistsError
from app.models.employee import EmployeeData
from app.repositories.interfaces.employee_repository_interface import EmployeeRepositoryInterface
from app.schemas.employee import EmployeeCreate

class EmployeeService:

    def __init__( self, repository: EmployeeRepositoryInterface, db: AsyncSession ) -> None:
        self.repository = repository
        self.db = db

    async def create_employee(self,employee: EmployeeCreate) -> EmployeeData:

        try:
            new_employee: EmployeeData = await self.repository.create_new_employee( employee )

            await self.db.commit()
            await self.db.refresh(new_employee)

            return new_employee

        except IntegrityError as exc:

            await self.db.rollback()
            raise EmployeeAlreadyExistsError() from exc
