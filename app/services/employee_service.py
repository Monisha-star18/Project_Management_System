
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.employee_exception import (
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    InvalidEmployeeUpdateError,
)
from app.models.employee import EmployeeData
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:

    def __init__( 
            self, 
            repository: EmployeeRepositoryInterface, 
            db: AsyncSession 
        ) -> None:

        self.repository = repository
        self.db = db

    async def create_employee(
            self,
            employee: EmployeeCreate
        ) -> EmployeeData:

        try:
            new_employee: EmployeeData = await self.repository.create_new_employee( employee )

            await self.db.commit()
            await self.db.refresh(new_employee)

            return new_employee

        except IntegrityError as exc:

            await self.db.rollback()
            raise EmployeeAlreadyExistsError() from exc

        
    async def get_all_employees( 
            self, 
            page: int, 
            size: int
        ) -> dict:

        employees, total = ( await self.repository.get_all_employees(page, size) )

        return {
            "pages": (total + size - 1) // size,
            "employees": employees
        }


    async def get_employee_by_id(
            self, 
            employee_id: int
        ) -> EmployeeData:

        employee = await self.repository.get_employee_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError()

        return employee


    async def update_employee(
        self, 
        employee_id: int, 
        data: EmployeeUpdate
    ) -> EmployeeData:

        employee = await self.get_employee_by_id(employee_id)

        update_data = data.model_dump(exclude_unset=True)

        if any(value is None for value in update_data.values()):
            raise InvalidEmployeeUpdateError()

        try:
            updated = await self.repository.update_employee(employee, update_data)

            await self.db.commit()
            await self.db.refresh(updated)

            return updated

        except IntegrityError as exc:
            await self.db.rollback()
            raise EmployeeAlreadyExistsError() from exc


    async def delete_employee(
            self, 
            employee_id: int
        ) -> dict:

        employee = await self.get_employee_by_id(employee_id)

        await self.repository.soft_delete_employee(employee)
        await self.db.commit()

        return {
            "message": "Employee deleted successfully",
            "employee_id": employee_id
        }

