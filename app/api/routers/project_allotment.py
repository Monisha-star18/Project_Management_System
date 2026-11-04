from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.api.dependency.auth import get_current_user, require_roles
from app.api.dependency.project_allotment_dependency import (
    get_project_allotment_service,
)
from app.models.employee import EmployeeData
from app.models.project_allotment import ProjectAllotment
from app.schemas.project_allotment import (
    AllotmentCreate,
    AllotmentListResponse,
    AllotmentResponse,
)
from app.services.project_allotment_service import ProjectAllotmentService

router = APIRouter(prefix="/api/projects", tags=["Project Allotments"])
ServiceDep = Annotated[ProjectAllotmentService, Depends(get_project_allotment_service)]
CurrentUserDep = Annotated[EmployeeData, Depends(get_current_user)]
LeadUserDep = Annotated[EmployeeData, Depends(require_roles("team_lead"))]
AllUserDep = Annotated[EmployeeData, Depends(require_roles("admin","team_lead","employee"))]
ProjectId = Annotated[int, Path(gt=0)]
EmployeeId = Annotated[int, Path(gt=0)]


@router.post(
    "/{project_id}/allotments",
    response_model=AllotmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Allot an employee to a project (project lead only)",
)
async def add_project_employee(
    project_id: ProjectId,
    data: AllotmentCreate,
    current_user: LeadUserDep,
    service: ServiceDep,
) -> AllotmentResponse:
    return await service.add_employee(project_id, data, current_user)


@router.get(
    "/{project_id}/allotments",
    response_model=AllotmentListResponse,
    summary="List employees allotted to a project",
)
async def list_project_employees(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    service: ServiceDep,
) -> AllotmentListResponse:
    return await service.list_members(project_id, current_user)


@router.delete(
    "/{project_id}/allotments/{employee_id}",
    summary="Remove an employee and delete their tasks in this project",
)
async def remove_project_employee(
    project_id: ProjectId,
    employee_id: EmployeeId,
    current_user: LeadUserDep,
    service: ServiceDep,
) -> dict[str, str | int]:
    return await service.remove_employee(project_id, employee_id, current_user)

@router.get(
    "/employees/{employee_id}/allotments",
    response_model=list[AllotmentResponse],
    summary="Get employee project allotments",
)
async def get_employee_allotments(
    employee_id: Annotated[int, Path(gt=0)],
    current_user: CurrentUserDep,
    service: ServiceDep,
) -> list[ProjectAllotment]:
    return await service.get_employee_allotments(
        employee_id=employee_id,
        current_user=current_user,
    )
