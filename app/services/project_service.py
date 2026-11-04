
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.auth_exception import PermissionDeniedError
from app.exceptions.project_exception import (
    InvalidProjectLeadError,
    InvalidProjectUpdateError,
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
)
from app.models.employee import EmployeeData
from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.repositories.interfaces.project_repository_interface import (
    ProjectRepositoryInterface,
)
from app.schemas.project import (
    PaginatedProjectResponse,
    ProjectCreate,
    ProjectLeadUpdate,
    ProjectResponse,
    ProjectUpdate,
)


class ProjectService:

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
        employee_repository: EmployeeRepositoryInterface,
        db: AsyncSession,
    ) -> None:

        self.repository = repository
        self.employee_repository = employee_repository
        self.db = db

    @staticmethod
    def _check_project_lead(
        current_user: EmployeeData,
        project: ProjectDetails,
    ) -> None:

        if not current_user.is_active:
            raise PermissionDeniedError()

        if project.lead_id == current_user.employee_id :
            return

        raise PermissionDeniedError()

    async def _validate_lead(
        self,
        lead_id: int,
    ) -> EmployeeData:

        employee = await self.employee_repository.get_employee_by_id(lead_id)

        if (
            employee is None
            or not employee.is_active
            or employee.role != "team_lead"
        ):
            raise InvalidProjectLeadError()

        return employee

    # CREATE PROJECT - ADMIN ONLY
    async def create_project(
        self,
        project: ProjectCreate,
        current_user: EmployeeData,
    ) -> ProjectDetails:

        try:
            new_project = await self.repository.create_new_project(
                project,
                current_user.employee_id
            )
            
            await self.db.commit()
            await self.db.refresh(new_project)

            return new_project

        except IntegrityError as exc:
            await self.db.rollback()
            raise ProjectAlreadyExistsError() from exc

        except Exception:
            await self.db.rollback()
            raise

    # GET PROJECT BY ID 
    async def get_project_by_id(
        self,
        project_id: int,
    ) -> ProjectDetails:

        project = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError()

        return project

    # GET ALL PROJECTS - ROLE BASED
    async def get_all_projects(
        self,
        page: int,
        size: int,
    )->ProjectDetails:

        return await self.repository.get_all_projects(page,size)

    # UPDATE PROJECT - ADMIN OR ASSIGNED PROJECT LEAD
    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
        current_user: EmployeeData,
    ) -> ProjectDetails:

        project = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError()

        self._check_project_lead(current_user,project)

        update_data = data.model_dump(exclude_unset=True)

        start_date = update_data.get("start_date",project.start_date)

        end_date = update_data.get("expected_end_date",project.expected_end_date)

        minimum_end_date = start_date + timedelta(days=7)

        if end_date < minimum_end_date:
            raise InvalidProjectUpdateError(
                "Project duration must be at least 7 days"
            )

        if not update_data:
            return project

        try:
            updated = await self.repository.update_project(project,update_data)

            await self.db.commit()
            await self.db.refresh(updated)

            return updated

        except IntegrityError as exc:
            await self.db.rollback()
            raise ProjectAlreadyExistsError() from exc

        except Exception:
            await self.db.rollback()
            raise

    # CHANGE PROJECT LEAD - ADMIN ONLY
    async def change_project_lead(
        self,
        project_id: int,
        data: ProjectLeadUpdate
    ) -> ProjectDetails:

        project = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError()

        old_project_lead_id = project.lead_id

        try:

            old_allotment = await self.db.scalar(
                select(ProjectAllotment).where(
                    ProjectAllotment.project_id == project_id,
                    ProjectAllotment.employee_id == old_project_lead_id,
                )
            )
            
            if old_allotment is not None:
                old_allotment.is_active = False
                old_allotment.remark_on_remove = data.remark_on_remove        

            allotment = await self.db.scalar(
                select(ProjectAllotment).where(
                    ProjectAllotment.project_id == project_id,
                    ProjectAllotment.employee_id == data.lead_id,
                )
            )

            if allotment is None:

                allotment = ProjectAllotment(
                    project_id=project_id,
                    employee_id=data.lead_id,
                )

                self.db.add(allotment)

            elif not allotment.is_active:
                allotment.is_active = True

            await self.db.flush()

            updated = await self.repository.update_project(project,{"lead_id": data.lead_id})

            await self.db.commit()
            await self.db.refresh(updated)

            return updated

        except Exception:
            await self.db.rollback()
            raise

    # DELETE PROJECT - ADMIN OR ASSIGNED PROJECT LEAD
    async def delete_project(
        self,
        project_id: int,
    ) -> dict[str, str | int]:

        project = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError()

        try:
            await self.repository.delete_project(project)

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

        return {
            "message": "Project deleted successfully",
            "project_id": project_id,
        }
