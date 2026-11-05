
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.employee import EmployeeData
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
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


    from sqlalchemy import select, func

    async def get_all_employees(self, page: int, size: int):

        query = (
            select(EmployeeData)
            .where(EmployeeData.is_active.is_(True))
            .order_by(EmployeeData.employee_id)
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await self.db.execute(query)

        count_result = await self.db.execute(
            select(func.count(EmployeeData.employee_id))
            .where(EmployeeData.is_active.is_(True))
        )

        employees = result.scalars().all()
        total = count_result.scalar_one()

        return employees, total


    async def get_employee_by_id(self, employee_id: int) -> EmployeeData | None:

        result = await self.db.execute(
            select(EmployeeData).where(
                EmployeeData.employee_id == employee_id,
                EmployeeData.is_active.is_(True)
            )
        )

        return result.scalar_one_or_none()

    async def update_employee( self, employee: EmployeeData, data: dict) -> EmployeeData:

        for field, value in data.items():
            setattr(employee, field, value)

        await self.db.flush()
        return employee


    async def soft_delete_employee(self, employee: EmployeeData) -> None:

        employee.is_active = False
        await self.db.flush()
