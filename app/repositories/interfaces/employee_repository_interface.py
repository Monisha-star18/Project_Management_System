
from abc import ABC, abstractmethod

from app.models.employee import EmployeeData
from app.schemas.employee import EmployeeCreate


class EmployeeRepositoryInterface(ABC):

    @abstractmethod
    async def create_new_employee(self, employee: EmployeeCreate) -> EmployeeData:
        pass

        
    @abstractmethod
    async def get_all_employees( self, page: int, size: int) -> tuple[list[EmployeeData], int]:
        pass

    @abstractmethod
    async def get_employee_by_id(self, employee_id: int) -> EmployeeData | None:
        pass

    @abstractmethod
    async def update_employee(self, employee: EmployeeData, data: dict) -> EmployeeData:
        pass

    @abstractmethod
    async def soft_delete_employee(self, employee: EmployeeData) -> None:
        pass

