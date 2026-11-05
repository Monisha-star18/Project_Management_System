from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.auth_exception import PermissionDeniedError
from app.exceptions.project_exception import ProjectNotFoundError
from app.exceptions.task_exception import (
    InvalidTaskUpdateError,
    TaskAssignmentError,
    TaskNotFoundError,
    TaskProjectAccessDeniedError,
)
from app.models.employee import EmployeeData
from app.models.project import ProjectDetails
from app.models.task import TaskDetails
from app.repositories.interfaces.task_repository_interface import (
    TaskRepositoryInterface,
)
from app.schemas.task import (
    TaskCreate,
    TaskProgressUpdate,
    TaskResponse,
    TaskUpdate,
)


class TaskService:

    def __init__(
        self,
        repository: TaskRepositoryInterface,
        db: AsyncSession
    ) -> None:
        self.repository = repository
        self.db = db

    def _lead(
        self,
        user: EmployeeData,
        project: ProjectDetails
    ) -> None:

        if not user.is_active:
            raise PermissionDeniedError()

        if project.lead_id != user.employee_id:
            raise TaskProjectAccessDeniedError()

    async def _project(
        self,
        project_id: int
    ) -> ProjectDetails:

        project = await self.repository.get_project(project_id)

        if project is None:
            raise ProjectNotFoundError()

        return project

    async def _task(
        self,
        task_id: int
    ) -> TaskDetails:

        task = await self.repository.get_task(task_id)

        if task is None:
            raise TaskNotFoundError()

        return task

    async def _allotment(
        self,
        project_id: int,
        employee_id: int
    ):

        allotment = await self.repository.get_allotment(
            project_id,
            employee_id
        )

        if allotment is None:
            raise TaskAssignmentError()

        return allotment

    @staticmethod
    def _response(task: TaskDetails) -> TaskResponse:

        return TaskResponse.model_validate({
            "task_id": task.task_id,
            "allotment_id": task.allotment_id,
            "project_id": task.allotment.project_id,
            "employee_id": task.allotment.employee_id,
            "task_title": task.task_title,
            "description": task.description,
            "assigned_by": task.assigned_by,
            "priority": task.priority,
            "start_date": task.start_date,
            "due_date": task.due_date,
            "status": task.status,
            "progress_percentage": task.progress_percentage,
            "remarks": task.remarks,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        })

    # CREATE TASK

    async def create(
        self,
        project_id: int,
        data: TaskCreate,
        user: EmployeeData
    ) -> TaskResponse:

        project = await self._project(project_id)

        self._lead(user, project)

        allotment = await self._allotment(
            project_id,
            data.employee_id
        )

        task = TaskDetails(
            allotment_id=allotment.allotment_id,
            assigned_by=user.employee_id,
            **data.model_dump(exclude={"employee_id"}),
        )

        try:
            await self.repository.add_task(task)

            created_id = task.task_id

            await self.db.commit()

            return self._response(
                await self._task(created_id)
            )

        except Exception:
            await self.db.rollback()
            raise

    # LIST PROJECT TASKS

    async def list_project(
        self,
        project_id: int,
        user: EmployeeData
    ) -> list[TaskResponse]:

        project = await self._project(project_id)

        if user.role == "team_lead":
            self._lead(user, project)


        tasks = await self.repository.list_tasks(
            project_id=project_id
        )

        return [
            self._response(task)
            for task in tasks
        ]

    # GET TASK

    async def get(
        self,
        task_id: int,
        user: EmployeeData
    ) -> TaskResponse:

        task = await self._task(task_id)

        project = await self._project(
            task.allotment.project_id
        )

        if user.role == "team_lead":
            self._lead(user, project)

        elif user.role == "employee":
            if (
                task.allotment.employee_id != user.employee_id
                or not task.allotment.is_active
            ):
                raise PermissionDeniedError()

        return self._response(task)

    # MY TASKS

    async def mine(
        self,
        user: EmployeeData
    ) -> list[TaskResponse]:

        tasks = await self.repository.list_tasks(
            employee_id=user.employee_id
        )

        return [
            self._response(task)
            for task in tasks
            if task.allotment.is_active
        ]

    # EMPLOYEE PROJECT TASKS

    async def project_employee(
        self,
        project_id: int,
        employee_id: int,
        user: EmployeeData
    ) -> list[TaskResponse]:

        project = await self._project(project_id)

        if user.role == "team_lead":
            self._lead(user, project)

        elif user.role == "employee":

            if user.employee_id != employee_id:
                raise PermissionDeniedError()

            allotment = await self.repository.get_allotment(
                project_id,
                employee_id
            )

            if allotment is None:
                raise PermissionDeniedError()

        tasks = await self.repository.list_tasks(
            project_id=project_id,
            employee_id=employee_id
        )

        return [
            self._response(task)
            for task in tasks
        ]

    # UPDATE TASK

    async def update(
        self,
        task_id: int,
        data: TaskUpdate,
        user: EmployeeData
    ) -> TaskResponse:

        task = await self._task(task_id)

        project = await self._project(
            task.allotment.project_id
        )

        self._lead(user, project)

        updates = data.model_dump(exclude_unset=True)

        for field in (
            "task_title",
            "priority",
            "start_date",
            "due_date"
        ):
            if field in updates and updates[field] is None:
                raise InvalidTaskUpdateError(
                    f"{field} cannot be null"
                )

        start = updates.get("start_date", task.start_date)
        due = updates.get("due_date", task.due_date)

        if due < start:
            raise InvalidTaskUpdateError(
                "due_date must be on or after start_date"
            )

        if "employee_id" in updates:

            if updates["employee_id"] is None:
                raise InvalidTaskUpdateError(
                    "employee_id cannot be null"
                )

            allotment = await self._allotment(
                project.project_id,
                updates.pop("employee_id")
            )

            task.allotment_id = allotment.allotment_id

        for field, value in updates.items():
            setattr(task, field, value)

        try:
            await self.db.commit()

            return self._response(
                await self._task(task_id)
            )

        except Exception:
            await self.db.rollback()
            raise

    # UPDATE TASK PROGRESS

    async def progress(
        self,
        task_id: int,
        data: TaskProgressUpdate,
        user: EmployeeData
    ) -> TaskResponse:

        task = await self._task(task_id)

        if (
            task.allotment.employee_id != user.employee_id
            or not task.allotment.is_active
        ):
            raise PermissionDeniedError()

        if data.progress_percentage == 100:
            new_status = data.status or "completed"

        else:
            new_status = data.status or (
                "todo"
                if data.progress_percentage == 0
                else "in_progress"
            )

        if (
            new_status == "completed"
            and data.progress_percentage != 100
        ):
            raise InvalidTaskUpdateError(
                "Completed tasks must have 100% progress"
            )

        if (
            new_status != "completed"
            and data.progress_percentage == 100
        ):
            raise InvalidTaskUpdateError(
                "100% progress requires completed status"
            )

        task.progress_percentage = data.progress_percentage
        task.status = new_status

        if "remarks" in data.model_fields_set:
            task.remarks = data.remarks

        try:
            await self.db.commit()

            return self._response(
                await self._task(task_id)
            )

        except Exception:
            await self.db.rollback()
            raise

    # DELETE TASK

    async def delete(
        self,
        task_id: int,
        user: EmployeeData
    ) -> dict[str, int | str]:

        task = await self._task(task_id)

        project = await self._project(
            task.allotment.project_id
        )

        self._lead(user, project)

        try:
            await self.repository.delete_task(task)
            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }