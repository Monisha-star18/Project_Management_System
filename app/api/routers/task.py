from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.api.dependency.auth import get_current_user, require_roles
from app.api.dependency.task_dependency import get_task_service
from app.models.employee import EmployeeData
from app.schemas.task import (
    TaskCreate,
    TaskProgressUpdate,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import TaskService


router = APIRouter(
    prefix="/api",
    tags=["Tasks"]
)


# Role dependencies

dependLead = [Depends(require_roles("team_lead"))]
dependLeadAdmin = [Depends(require_roles("team_lead", "admin"))]
dependAll = [Depends(require_roles("admin", "employee", "team_lead"))]
dependEmployee = [Depends(require_roles("employee"))]


# Common dependencies
ServiceDep = Annotated[TaskService,Depends(get_task_service)]
CurrentUserDep = Annotated[EmployeeData,Depends(get_current_user)]

ProjectId = Annotated[int, Path(gt=0)]
TaskId = Annotated[int, Path(gt=0)]
EmployeeId = Annotated[int, Path(gt=0)]


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependLead,
    summary="Create project task (project lead only)"
)
async def create_task(
    project_id: ProjectId,
    data: TaskCreate,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> TaskResponse:

    return await service.create(project_id, data, current_user)


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse],
    dependencies=dependLeadAdmin,
    summary="List project tasks (project lead or admin)"
)
async def list_project_tasks(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> list[TaskResponse]:

    return await service.list_project(project_id, current_user)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    dependencies=dependAll,
    summary="Get task (project lead, assignee or admin)"
)
async def get_task(
    task_id: TaskId,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> TaskResponse:

    return await service.get(task_id, current_user)


@router.get(
    "/employees/me/tasks",
    response_model=list[TaskResponse],
    dependencies=dependEmployee,
    summary="Get my assigned tasks"
)
async def get_my_tasks(
    current_user: CurrentUserDep,
    service: ServiceDep
) -> list[TaskResponse]:

    return await service.mine(current_user)


@router.get(
    "/projects/{project_id}/employees/{employee_id}/tasks",
    response_model=list[TaskResponse],
    dependencies=dependAll,
    summary="Get tasks for an employee within a project"
)
async def get_employee_project_tasks(
    project_id: ProjectId,
    employee_id: EmployeeId,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> list[TaskResponse]:

    return await service.project_employee(
        project_id,
        employee_id,
        current_user
    )


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    dependencies=dependLead,
    summary="Update task (project lead only)"
)
async def update_task(
    task_id: TaskId,
    data: TaskUpdate,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> TaskResponse:

    return await service.update(task_id, data, current_user)


@router.patch(
    "/tasks/{task_id}/progress",
    response_model=TaskResponse,
    dependencies=dependEmployee,
    summary="Update task progress (assigned employee only)"
)
async def update_task_progress(
    task_id: TaskId,
    data: TaskProgressUpdate,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> TaskResponse:

    return await service.progress(task_id, data, current_user)


@router.delete(
    "/tasks/{task_id}",
    dependencies=dependLead,
    summary="Delete task (project lead only)"
)
async def delete_task(
    task_id: TaskId,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> dict[str, int | str]:

    return await service.delete(task_id, current_user)