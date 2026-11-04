
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.repositories.interfaces.project_repository_interface import (
    ProjectRepositoryInterface,
)
from app.schemas.project import ProjectCreate


class ProjectRepository(ProjectRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_new_project(
        self,
        project: ProjectCreate,
        created_by: int,
    ) -> ProjectDetails:
        
        new_project = ProjectDetails(
            **project.model_dump(),
            created_by=created_by,
        )

        self.db.add(new_project)
        await self.db.flush()

        return new_project

    async def get_project_by_id(
        self,
        project_id: int,
    ) -> ProjectDetails | None:
        result = await self.db.execute(
            select(ProjectDetails).where(
                ProjectDetails.project_id == project_id
            )
        )

        return result.scalar_one_or_none()

    async def get_project_by_name(
        self,
        project_name: str,
    ) -> ProjectDetails | None:
        result = await self.db.execute(
            select(ProjectDetails).where(
                ProjectDetails.project_name == project_name
            )
        )

        return result.scalar_one_or_none()

    async def get_all_projects(
        self,
        page: int,
        size: int,
        lead_id: int | None = None,
        created_by: int | None = None,
        member_employee_id: int | None = None,
    ) -> tuple[list[ProjectDetails], int]:
        conditions = []

        if lead_id is not None:
            conditions.append(
                ProjectDetails.lead_id == lead_id
            )

        if created_by is not None:
            conditions.append(
                ProjectDetails.created_by == created_by
            )

        if member_employee_id is not None:
            membership_exists = (
                select(ProjectAllotment.allotment_id)
                .where(
                    ProjectAllotment.project_id
                    == ProjectDetails.project_id,
                    ProjectAllotment.employee_id
                    == member_employee_id,
                    ProjectAllotment.is_active.is_(True),
                )
                .exists()
            )

            conditions.append(membership_exists)

        query = (
            select(ProjectDetails)
            .where(*conditions)
            .order_by(ProjectDetails.project_id)
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await self.db.execute(query)

        count_query = (
            select(func.count(ProjectDetails.project_id))
            .where(*conditions)
        )

        total = await self.db.scalar(count_query)

        return list(result.scalars().all()), total or 0

    async def update_project(
        self,
        project: ProjectDetails,
        data: dict[str, Any],
    ) -> ProjectDetails:
        for field, value in data.items():
            setattr(project, field, value)

        await self.db.flush()

        return project

    async def delete_project(
        self,
        project: ProjectDetails,
    ) -> None:
        await self.db.delete(project)
        await self.db.flush()
