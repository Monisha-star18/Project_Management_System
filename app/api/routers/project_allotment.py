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
from fastapi import BackgroundTasks

from app.api.dependency.employee_dependency import get_employee_service
from app.services.employee_service import EmployeeService
from app.services.email.project_allotted_email import ProjectAllottedEmail

router = APIRouter(
    prefix="/api/projects", 
    tags=["Project Allotments"]
)


dependLead = [Depends(require_roles("team_lead"))]
dependAll = [Depends(require_roles("admin", "employee", "team_lead"))]


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
    dependencies=dependLead,
    summary="Allot an employee to a project (project lead only)",
    description="Assigned project team lead only. Allot an active employee to a project. Prevents duplicate allotments and sends an email notification to the employee after successful assignment."
)
async def add_project_employee(
    project_id: ProjectId,
    data: AllotmentCreate,
    background_tasks: BackgroundTasks,
    current_user: LeadUserDep,
    service: ServiceDep,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> AllotmentResponse:

    allotment = await service.add_employee(project_id, data, current_user)

    employee = await employee_service.get_employee_by_id(data.employee_id)

    email_service = ProjectAllottedEmail(
        project_id=project_id,
        lead_name=current_user.full_name,
    )

    background_tasks.add_task(
        email_service.send,
        employee.email,
        employee.full_name,
    )

    return allotment


@router.get(
    "/{project_id}/allotments",
    response_model=AllotmentListResponse,
    dependencies = dependAll,
    summary="List employees allotted to a project",
    description="Retrieve all active employees allotted to a specific project, including their employee details and total member count. Accessible to admins, team leads and employees."

)
async def list_project_employees(
    project_id: ProjectId,
    service: ServiceDep,
) -> AllotmentListResponse:
    
    return await service.list_members(project_id)


@router.get(
    "/employees/{employee_id}/allotments",
    response_model=list[AllotmentResponse],
    dependencies = dependAll,
    summary="Get employee project allotments",
    description="Retrieve all project allotments associated with a specific employee using their employee ID. Accessible to authenticated admins, team leads and employees."
)
async def get_employee_allotments(
    employee_id: Annotated[int, Path(gt=0)],
    service: ServiceDep,
) -> list[ProjectAllotment]:
    
    return await service.get_employee_allotments(employee_id)


@router.delete(
    "/{project_id}/allotments/{employee_id}",
    dependencies = dependLead,
    summary="Remove an employee and delete their tasks in this project",
    description="Team lead only. Remove an employee from a specified project allotment and delete their associated project tasks. The current project lead cannot be removed through this endpoint."
)
async def remove_project_employee(
    project_id: ProjectId,
    employee_id: EmployeeId,
    current_user: LeadUserDep,
    service: ServiceDep,
) -> dict[str, str | int]:
    
    return await service.remove_employee(project_id, employee_id, current_user)

