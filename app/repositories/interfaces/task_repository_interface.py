from abc import ABC, abstractmethod

from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.models.task import TaskDetails


class TaskRepositoryInterface(ABC):
    @abstractmethod
    async def get_project(self, project_id: int) -> ProjectDetails | None: ...

    @abstractmethod
    async def get_allotment(self, project_id: int, employee_id: int) -> ProjectAllotment | None: ...

    @abstractmethod
    async def get_task(self, task_id: int) -> TaskDetails | None: ...

    @abstractmethod
    async def list_tasks(self, *, project_id: int | None = None, employee_id: int | None = None) -> list[TaskDetails]: ...

    @abstractmethod
    async def add_task(self, task: TaskDetails) -> TaskDetails: ...

    @abstractmethod
    async def delete_task(self, task: TaskDetails) -> None: ...
