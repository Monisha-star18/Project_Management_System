from pydantic import BaseModel

from app.schemas.project import ProjectResponse


class ProjectReportResponse(BaseModel):
    project: ProjectResponse
    total_employees: int
    total_tasks: int
    completed_tasks: int
    completion_percentage: float