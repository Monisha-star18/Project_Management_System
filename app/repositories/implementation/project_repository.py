
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import ProjectDetails
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
            select(ProjectDetails).where(ProjectDetails.project_id == project_id)
        )

        return result.scalar_one_or_none()


    async def get_all_projects(
        self,
        page: int,
        size: int,
    )->ProjectDetails :
        query = (
            select(ProjectDetails)
            .order_by(ProjectDetails.project_id)
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await self.db.execute(query)

        return list(result.scalars().all()) 

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
