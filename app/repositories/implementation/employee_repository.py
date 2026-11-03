
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.employee import EmployeeData
from app.repositories.interfaces.employee_repository_interface import EmployeeRepositoryInterface
from app.schemas.employee import EmployeeCreate


class EmployeeRepository(EmployeeRepositoryInterface):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_new_employee(self,employee: EmployeeCreate) -> EmployeeData:

       data = employee.model_dump(exclude={"password"})
       
       new_employee = EmployeeData(
          **data,
            password_hash=hash_password(employee.password)
        )
       
       self.db.add(new_employee)
       await self.db.flush()
       
       return new_employee
