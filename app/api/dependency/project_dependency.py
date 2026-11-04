
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependency.employee_dependency import (
    get_employee_repository,
)
from app.database.session import get_session
from app.repositories.implementation.project_repository import (
    ProjectRepository,
)
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.repositories.interfaces.project_repository_interface import (
    ProjectRepositoryInterface,
)
from app.services.project_service import ProjectService


def get_project_repository(db:AsyncSession= Depends(get_session)) -> ProjectRepositoryInterface:
    
    return ProjectRepository(db)


def get_project_service(
    repository:ProjectRepositoryInterface= Depends(get_project_repository),
    employee_repository: EmployeeRepositoryInterface = Depends(get_employee_repository),
    db:AsyncSession = Depends(get_session),
) -> ProjectService:
    
    return ProjectService(
        repository=repository,
        employee_repository=employee_repository,
        db=db,
    )
