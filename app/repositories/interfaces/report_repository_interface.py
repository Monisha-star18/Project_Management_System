from abc import ABC, abstractmethod

from app.models.project import ProjectDetails


class ReportRepositoryInterface(ABC):

    @abstractmethod
    async def get_project(
        self, project_id: int
    ) -> ProjectDetails | None:
        pass