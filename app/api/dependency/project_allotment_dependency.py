from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependency.employee_dependency import get_employee_repository
from app.database.session import get_session
from app.repositories.implementation.project_allotment_repository import (
    ProjectAllotmentRepository,
)
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.repositories.interfaces.project_allotment_repository_interface import (
    ProjectAllotmentRepositoryInterface,
)
from app.services.project_allotment_service import ProjectAllotmentService


def get_project_allotment_repository(
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProjectAllotmentRepositoryInterface:
    return ProjectAllotmentRepository(db)


def get_project_allotment_service(
    repository: Annotated[
        ProjectAllotmentRepositoryInterface,
        Depends(get_project_allotment_repository),
    ],
    employee_repository: Annotated[
        EmployeeRepositoryInterface,
        Depends(get_employee_repository),
    ],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> ProjectAllotmentService:
    return ProjectAllotmentService(repository, employee_repository, db)
