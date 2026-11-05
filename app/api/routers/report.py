from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.api.dependency.auth import require_roles
from app.api.dependency.report_dependency import get_report_service
from app.schemas.report import ProjectReportResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


dependAll = [
    Depends(require_roles("admin", "team_lead","employee"))
]


# GET PROJECT REPORT BY ID
@router.get(
    "/projects/{project_id}",
    response_model=ProjectReportResponse,
    dependencies=dependAll,
    summary="Get project report",
    description="Generate a detailed project report containing project information, total active allotted employees, total tasks, completed tasks, task completion percentage and overall project progress percentage calculated from the average progress of all project tasks. Accessible to admins, team leads and employees."
)
async def get_project_report(
    service: Annotated[ReportService, Depends(get_report_service)],
    project_id: int = Path(..., gt=0),
    
) -> dict:

    return await service.get_project_report(project_id)