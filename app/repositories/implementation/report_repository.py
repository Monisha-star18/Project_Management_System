from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.repositories.interfaces.report_repository_interface import (
    ReportRepositoryInterface,
)


class ReportRepository(ReportRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_project(
        self, project_id: int
    ) -> ProjectDetails | None:

        query = (
            select(ProjectDetails)
            .options(
                selectinload(ProjectDetails.allotments)
                .selectinload(ProjectAllotment.tasks)
            )
            .where(ProjectDetails.project_id == project_id)
        )

        return await self.db.scalar(query)