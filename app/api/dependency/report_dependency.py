from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.interfaces.report_repository_interface import (
    ReportRepositoryInterface,
)
from app.repositories.implementation.report_repository import ReportRepository
from app.services.report_service import ReportService


def get_report_repository(
    db: AsyncSession = Depends(get_session)
) -> ReportRepositoryInterface:
    return ReportRepository(db)


def get_report_service(
    repository: ReportRepositoryInterface = Depends(get_report_repository)
) -> ReportService:
    return ReportService(repository)