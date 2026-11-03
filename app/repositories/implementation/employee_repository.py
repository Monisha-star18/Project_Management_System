
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import EmployeeData
from app.repositories.interfaces.employee_repository_interface import EmployeeRepositoryInterface
from app.schemas.employee import EmployeeCreate


class EmployeeRepository(EmployeeRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_new_employee(self,employee: EmployeeCreate) -> EmployeeData:

        new_employee: EmployeeData = EmployeeData(
            **employee.model_dump()
        )

        self.db.add(new_employee)
        await self.db.flush()

        return new_employee
