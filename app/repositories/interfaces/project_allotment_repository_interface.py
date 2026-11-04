from abc import ABC, abstractmethod

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment


class ProjectAllotmentRepositoryInterface(ABC):
    @abstractmethod
    async def get_project_with_members(self, project_id: int) -> ProjectDetails | None:
        """Load a project and its allotments with their employees."""
        ...

    @abstractmethod
    async def get_membership(
        self, project_id: int, employee_id: int
    ) -> ProjectAllotment | None:
        """Find one membership, with its related employee."""
        ...

    @abstractmethod
    async def add_member(self, project_id: int, employee_id: int) -> ProjectAllotment:
        """Insert an allotment and flush, without committing."""
        ...

    @abstractmethod
    async def remove_member(self, allotment: ProjectAllotment) -> None:
        """Delete an allotment and flush, without committing."""
        ...

    @abstractmethod
    async def get_employee_allotments(
        self,
        employee_id: int,
    ) -> list[ProjectAllotment]:
        """Retrieve all active project allotments for an employee."""
        ...