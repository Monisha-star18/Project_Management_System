
from abc import ABC, abstractmethod
from typing import Any

from app.models.project import ProjectDetails
from app.schemas.project import ProjectCreate


class ProjectRepositoryInterface(ABC):

    @abstractmethod
    async def create_new_project(
        self,
        project: ProjectCreate,
        created_by: int,
    ) -> ProjectDetails:
        """Add a new project to the database."""
        ...

    @abstractmethod
    async def get_project_by_id(
        self,
        project_id: int,
    ) -> ProjectDetails | None:
        """Retrieve a project by its ID."""
        ...

   
    @abstractmethod
    async def get_all_projects(
        self,
        page: int,
        size: int,
        lead_id: int | None = None,
        created_by: int | None = None,
        member_employee_id: int | None = None,
    ) -> tuple[list[ProjectDetails], int]:
        """Retrieve paginated projects with optional filters."""
        ...

    @abstractmethod
    async def update_project(
        self,
        project: ProjectDetails,
        data: dict[str, Any],
    ) -> ProjectDetails:
        """Update an existing project."""
        ...

    @abstractmethod
    async def delete_project(
        self,
        project: ProjectDetails,
    ) -> None:
        """Delete an existing project."""
        ...
