from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.implementation.task_repository import TaskRepository
from app.repositories.interfaces.task_repository_interface import (
    TaskRepositoryInterface,
)
from app.services.task_service import TaskService


def get_task_repository(
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRepositoryInterface:
    return TaskRepository(db)


def get_task_service(
    repository: Annotated[
        TaskRepositoryInterface,
        Depends(get_task_repository),
    ],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> TaskService:
    return TaskService(repository, db)