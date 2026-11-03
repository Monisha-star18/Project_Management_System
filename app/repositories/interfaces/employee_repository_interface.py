
from abc import ABC, abstractmethod

from app.models.employee import EmployeeData
from app.schemas.employee import EmployeeCreate


class EmployeeRepositoryInterface(ABC):

    @abstractmethod
    async def create_new_employee(self, employee: EmployeeCreate) -> EmployeeData:
        pass
