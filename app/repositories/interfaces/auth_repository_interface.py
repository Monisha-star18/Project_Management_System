
from abc import ABC, abstractmethod

from app.models.employee import EmployeeData


class AuthRepositoryInterface(ABC):

    @abstractmethod
    async def get_employee_by_email( self, email_id:str ) -> EmployeeData | None:
        pass
