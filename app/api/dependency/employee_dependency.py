from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.implementation.employee_repository import EmployeeRepository
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.services.employee_service import EmployeeService


def get_employee_repository(
    db: Annotated[AsyncSession, Depends(get_session)]
) -> EmployeeRepositoryInterface:

    return EmployeeRepository(db)


def get_employee_service(
    repository: Annotated[EmployeeRepositoryInterface,Depends(get_employee_repository),],
    db: Annotated[AsyncSession, Depends(get_session)]
) -> EmployeeService:

    return EmployeeService(repository, db)
