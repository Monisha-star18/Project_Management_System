from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.repositories.interfaces.project_allotment_repository_interface import (
    ProjectAllotmentRepositoryInterface,
)


class ProjectAllotmentRepository(ProjectAllotmentRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_project_with_members(self, project_id: int) -> ProjectDetails | None:
        stmt = (
            select(ProjectDetails)
            .options(
                selectinload(ProjectDetails.allotments).joinedload(
                    ProjectAllotment.employee
                )
            )
            .where(ProjectDetails.project_id == project_id)
        )
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def get_membership(
        self, project_id: int, employee_id: int
    ) -> ProjectAllotment | None:
        stmt = (
            select(ProjectAllotment)
            .options(joinedload(ProjectAllotment.employee))
            .where(
                ProjectAllotment.project_id == project_id,
                ProjectAllotment.employee_id == employee_id,
            )
        )
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def add_member(self, project_id: int, employee_id: int) -> ProjectAllotment:
        allotment = ProjectAllotment(project_id=project_id, employee_id=employee_id)
        self.db.add(allotment)
        await self.db.flush()
        return allotment

    async def remove_member(self, allotment: ProjectAllotment) -> None:
        await self.db.delete(allotment)
        await self.db.flush()

    async def get_employee_allotments(
        self,
        employee_id: int,
    ) -> list[ProjectAllotment]:
        stmt = (
            select(ProjectAllotment)
            .options(
                joinedload(ProjectAllotment.employee),
                joinedload(ProjectAllotment.project)
            )
            .where(
                ProjectAllotment.employee_id == employee_id,
                ProjectAllotment.is_active.is_(True),
            )
            .order_by(ProjectAllotment.allotted_at.desc())
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())
