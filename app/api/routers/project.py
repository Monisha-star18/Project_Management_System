
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.api.dependency.auth import get_current_user, require_roles
from app.api.dependency.project_dependency import get_project_service
from app.models.employee import EmployeeData
from app.models.project import ProjectDetails
from app.schemas.project import (
    PaginatedProjectResponse,
    ProjectCreate,
    ProjectLeadUpdate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)

ProjectServiceDep = Annotated[
    ProjectService,
    Depends(get_project_service),
]

CurrentUserDep = Annotated[
    EmployeeData,
    Depends(get_current_user),
]

AdminUserDep = Annotated[
    EmployeeData,
    Depends(require_roles("admin")),
]

ProjectId = Annotated[
    int,
    Path(gt=0),
]


# CREATE PROJECT - ADMIN ONLY
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
)
async def create_project(
    project: ProjectCreate,
    current_user: AdminUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    return await service.create_project(
        project=project,
        current_user=current_user,
    )


# GET ALL PROJECTS - ROLE-BASED VISIBILITY
@router.get(
    "/",
    response_model=PaginatedProjectResponse,
    summary="Get all accessible projects",
)
async def get_all_projects(
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> PaginatedProjectResponse:
    return await service.get_all_projects(
        page=page,
        size=size,
        current_user=current_user,
    )


# GET PROJECT BY ID
@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
)
async def get_project_by_id(
    project_id: ProjectId,
    current_user: CurrentUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    return await service.get_project_by_id(
        project_id=project_id,
        current_user=current_user,
    )


# UPDATE PROJECT - ADMIN ONLY
@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project details",
)
async def update_project(
    project_id: ProjectId,
    project: ProjectUpdate,
    current_user: AdminUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    return await service.update_project(
        project_id=project_id,
        data=project,
        current_user=current_user,
    )


# CHANGE PROJECT LEAD - ADMIN ONLY
@router.patch(
    "/{project_id}/lead",
    response_model=ProjectResponse,
    summary="Change project team lead",
)
async def change_project_lead(
    project_id: ProjectId,
    data: ProjectLeadUpdate,
    current_user: AdminUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    return await service.change_project_lead(
        project_id=project_id,
        data=data,
        current_user=current_user,
    )


# DELETE PROJECT - ADMIN ONLY
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a project",
)
async def delete_project(
    project_id: ProjectId,
    current_user: AdminUserDep,
    service: ProjectServiceDep,
) -> dict[str, str | int]:
    return await service.delete_project(
        project_id=project_id,
        current_user=current_user,
    )
