from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.models.task import TaskDetails
from app.repositories.interfaces.task_repository_interface import (
    TaskRepositoryInterface,
)


class TaskRepository(TaskRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_project(self, project_id: int) -> ProjectDetails | None:
        return await self.db.scalar(select(ProjectDetails).where(ProjectDetails.project_id == project_id))

    async def get_allotment(self, project_id: int, employee_id: int) -> ProjectAllotment | None:
        return await self.db.scalar(
            select(ProjectAllotment).where(
                ProjectAllotment.project_id == project_id,
                ProjectAllotment.employee_id == employee_id,
                ProjectAllotment.is_active.is_(True),
            )
        )

    async def get_task(self, task_id: int) -> TaskDetails | None:
        return await self.db.scalar(
            select(TaskDetails).options(joinedload(TaskDetails.allotment)).where(TaskDetails.task_id == task_id)
        )

    async def list_tasks(self, *, project_id: int | None = None, employee_id: int | None = None) -> list[TaskDetails]:
        query = select(TaskDetails).join(TaskDetails.allotment).options(joinedload(TaskDetails.allotment))
        if project_id is not None:
            query = query.where(ProjectAllotment.project_id == project_id)
        if employee_id is not None:
            query = query.where(ProjectAllotment.employee_id == employee_id)
        query = query.order_by(TaskDetails.task_id)
        return list((await self.db.scalars(query)).all())

    async def add_task(self, task: TaskDetails) -> TaskDetails:
        self.db.add(task)
        await self.db.flush()
        return task

    async def delete_task(self, task: TaskDetails) -> None:
        await self.db.delete(task)
        await self.db.flush()
