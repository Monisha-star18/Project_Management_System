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
from fastapi import BackgroundTasks

from app.api.dependency.employee_dependency import get_employee_service
from app.services.employee_service import EmployeeService
from app.services.email.task_assigned_email import TaskAssignedEmail


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


EmployeeServiceDep = Annotated[
    EmployeeService,
    Depends(get_employee_service),
]

@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependLead,
    summary="Create project task (project lead only)",
    description="Assigned project team lead only. Create a task for an employee already allotted to the project. Stores task details, priority, dates and assigned team lead information, and sends a task assignment email notification."
)
async def create_task(
    project_id: ProjectId,
    data: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: CurrentUserDep,
    service: ServiceDep,
    employee_service: EmployeeServiceDep,
) -> TaskResponse:

    task = await service.create(
        project_id, data, current_user
    )

    employee = await employee_service.get_employee_by_id(
        data.employee_id
    )

    email_service = TaskAssignedEmail(
        project_id=project_id,
        task_title=task.task_title,
        priority=task.priority,
        start_date=task.start_date,
        due_date=task.due_date,
        lead_name=current_user.full_name,
    )

    background_tasks.add_task(
        email_service.send,
        employee.email,
        employee.full_name,
    )

    return task

@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse],
    dependencies=dependAll,
    summary="List project tasks ",
    description="Retrieve all tasks belonging to a specific project. Admins can view project tasks, while team leads can view tasks only for projects assigned to them."
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
    summary="Get task (project lead, assignee or admin)",
    description="Retrieve complete details of a specific task using its task ID. Accessible to admins, the assigned project team lead and the employee assigned to the task."
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
    summary="Get my assigned tasks",
    description="Employee only. Retrieve all tasks assigned to the currently authenticated employee through their active project allotments."

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
    summary="Get tasks for an employee within a project",
    description="Retrieve tasks assigned to a specific employee within a particular project. Accessible to admins, the assigned project team lead and the employee viewing their own tasks."
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
    summary="Update task (project lead only)",
    description="Assigned project team lead only. Update task information including title, description, priority, dates or assigned employee. Reassignment requires the employee to have a valid project allotment."
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
    summary="Update task progress (assigned employee only)",
    description="Assigned employee only. Update the progress percentage, status and remarks of an assigned task. A completed task must have 100 percent progress, and 100 percent progress requires completed status."
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
    summary="Delete task (project lead only)",
    description="Assigned project team lead only. Permanently delete a task using its task ID. Team leads cannot delete tasks belonging to projects assigned to another team lead."
)
async def delete_task(
    task_id: TaskId,
    current_user: CurrentUserDep,
    service: ServiceDep
) -> dict[str, int | str]:

    return await service.delete(task_id, current_user)