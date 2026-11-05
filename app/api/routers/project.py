
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

ProjectServiceDep = Annotated[ ProjectService, Depends(get_project_service)]
CurrentUserDep = Annotated[ EmployeeData, Depends(get_current_user)]


dependAdmin = [Depends(require_roles("admin"))]
dependAdmin_Lead = [Depends(require_roles("admin","team_lead"))]
dependAll = [Depends(require_roles("admin", "employee", "team_lead"))]

AdminUserDep = Annotated[ EmployeeData,Depends(require_roles("admin"))]
AdminLeadUserDep = Annotated[EmployeeData,Depends(require_roles("admin", "team_lead"))]

ProjectId = Annotated[int, Path(gt=0)]

# CREATE PROJECT - ADMIN ONLY
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies = dependAdmin,
    summary="Create a new project",
    description="Admin only. Create a new project with its name, description, start date, end date and assigned team lead. The selected project lead must be a valid team lead."
)
async def create_project(
    project: ProjectCreate,
    current_user: AdminUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    
    return await service.create_project(project,current_user)


# GET PROJECT BY ID
@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies = dependAll,
    summary="Get project by ID",
    description="Retrieve the details of a specific project using its project ID. Accessible to authenticated admins, team leads and employees."
)
async def get_project_by_id(
    project_id: ProjectId,
    service: ProjectServiceDep,
) -> ProjectDetails:
    
    return await service.get_project_by_id(project_id)


# GET ALL PROJECTS - ROLE-BASED VISIBILITY
@router.get(
    "/",
    response_model=list[ProjectResponse],
    dependencies = dependAll,
    summary="Get all accessible projects",
    description="Retrieve a paginated list of projects. Accessible to authenticated admins, team leads and employees. Supports page and size query parameters."
)
async def get_all_projects(
    service: ProjectServiceDep,
    page: Annotated[int, Query(ge=1,le=100)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
)->ProjectDetails:
    
    return await service.get_all_projects(page,size)


# UPDATE PROJECT - ADMIN ONLY
@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    dependencies = dependAdmin_Lead,
    summary="Update project details",
    description="Update an existing project's details such as its name, description and dates. Accessible to admins and team leads, subject to project ownership validation."
)
async def update_project(
    project_id: ProjectId,
    project: ProjectUpdate,
    current_user: AdminLeadUserDep,
    service: ProjectServiceDep,
) -> ProjectDetails:
    
    return await service.update_project( project_id, project, current_user)


# CHANGE PROJECT LEAD - ADMIN ONLY
@router.patch(
    "/{project_id}/lead",
    response_model=ProjectResponse,
    dependencies = dependAdmin,
    summary="Change project team lead",
    description="Admin only. Change the assigned team lead of an existing project. The new project lead must be a valid and active employee with the team_lead role."
)
async def change_project_lead(
    project_id: ProjectId,
    data: ProjectLeadUpdate,
    service: ProjectServiceDep,
) -> ProjectDetails:
    
    return await service.change_project_lead(project_id,data)


# DELETE PROJECT - ADMIN ONLY
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    dependencies = dependAdmin,
    summary="Delete a project",
    description="Admin only. Delete an existing project using its project ID. Related project records may be affected according to the configured database relationships."
)
async def delete_project(
    project_id: ProjectId,
    service: ProjectServiceDep,
) -> dict[str, str | int]:
    
    return await service.delete_project(project_id)
