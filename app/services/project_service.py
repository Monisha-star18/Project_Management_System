
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
    def _require_admin(current_user: EmployeeData) -> None:
        if not current_user.is_active or current_user.role != "admin":
            raise PermissionDeniedError()

    async def _validate_lead(
        self,
        lead_id: int,
    ) -> EmployeeData:
        employee = await self.employee_repository.get_employee_by_id(
            lead_id
        )

        if (
            employee is None
            or not employee.is_active
            or employee.role != "team_lead"
        ):
            raise InvalidProjectLeadError()

        return employee

    @staticmethod
    def _handle_integrity_error(exc: IntegrityError) -> None:
        # PostgreSQL unique constraint on project_name.
        original = exc.orig
        diagnostic = getattr(original, "diag", None)

        constraint_name = getattr(
            diagnostic,
            "constraint_name",
            None,
        )

        if constraint_name == "uq_project_name":
            raise ProjectAlreadyExistsError() from exc

        # Preserve unexpected foreign-key/check constraint errors.
        raise exc

    async def create_project(
        self,
        project: ProjectCreate,
        current_user: EmployeeData,
    ) -> ProjectDetails:
        self._require_admin(current_user)
        await self._validate_lead(project.lead_id)

        try:
            new_project = await self.repository.create_new_project(
                project=project,
                created_by=current_user.employee_id,
            )

            # Every project lead must also be allotted.
            lead_allotment = ProjectAllotment(
                project_id=new_project.project_id,
                employee_id=project.lead_id,
            )

            self.db.add(lead_allotment)
            await self.db.flush()

            await self.db.commit()
            await self.db.refresh(new_project)

            return new_project

        except IntegrityError as exc:
            await self.db.rollback()
            self._handle_integrity_error(exc)
            raise  # Defensive fallback for static analysis.

        except Exception:
            await self.db.rollback()
            raise

    async def get_project_by_id(
        self,
        project_id: int,
        current_user: EmployeeData,
    ) -> ProjectDetails:
        project = await self.repository.get_project_by_id(
            project_id
        )

        if project is None:
            raise ProjectNotFoundError()

        if not current_user.is_active:
            raise PermissionDeniedError()

        if current_user.role == "admin":
            return project

        if (
            current_user.role == "team_lead"
            and project.lead_id == current_user.employee_id
        ):
            return project

        # Check membership without loading lazy ORM relationships.
        membership = await self.db.scalar(
            select(ProjectAllotment.allotment_id).where(
                ProjectAllotment.project_id == project_id,
                ProjectAllotment.employee_id
                == current_user.employee_id,
                ProjectAllotment.is_active.is_(True),
            )
        )

        if membership is None:
            raise PermissionDeniedError()

        return project

    async def get_all_projects(
        self,
        page: int,
        size: int,
        current_user: EmployeeData,
    ) -> PaginatedProjectResponse:
        if not current_user.is_active:
            raise PermissionDeniedError()

        if page < 1 or not 1 <= size <= 100:
            raise InvalidProjectUpdateError(
                "Page must be >= 1 and size must be between 1 and 100"
            )

        if current_user.role == "admin":
            projects, total = await self.repository.get_all_projects(
                page=page,
                size=size,
            )

        elif current_user.role == "team_lead":
            projects, total = await self.repository.get_all_projects(
                page=page,
                size=size,
                lead_id=current_user.employee_id,
            )

        elif current_user.role == "employee":
            projects, total = await self.repository.get_all_projects(
                page=page,
                size=size,
                member_employee_id=current_user.employee_id,
            )

        else:
            raise PermissionDeniedError()

        return PaginatedProjectResponse(
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
            projects=projects,
        )

    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
        current_user: EmployeeData,
    ) -> ProjectDetails:
        self._require_admin(current_user)

        project = await self.repository.get_project_by_id(
            project_id
        )
        if project is None:
            raise ProjectNotFoundError()

        update_data = data.model_dump(exclude_unset=True)

        required_fields = {
            "project_name",
            "start_date",
            "expected_end_date",
            "status",
        }

        for field in required_fields:
            if field in update_data and update_data[field] is None:
                raise InvalidProjectUpdateError(
                    f"{field} cannot be null"
                )

        start_date = update_data.get(
            "start_date",
            project.start_date,
        )
        end_date = update_data.get(
            "expected_end_date",
            project.expected_end_date,
        )

        if end_date < start_date:
            raise InvalidProjectUpdateError(
                "Expected end date cannot be before start date"
            )

        if not update_data:
            return project

        try:
            updated = await self.repository.update_project(
                project,
                update_data,
            )

            await self.db.commit()
            await self.db.refresh(updated)

            return updated

        except IntegrityError as exc:
            await self.db.rollback()
            self._handle_integrity_error(exc)
            raise

        except Exception:
            await self.db.rollback()
            raise

    async def change_project_lead(
        self,
        project_id: int,
        data: ProjectLeadUpdate,
        current_user: EmployeeData,
    ) -> ProjectDetails:
        self._require_admin(current_user)

        project = await self.repository.get_project_by_id(
            project_id
        )
        if project is None:
            raise ProjectNotFoundError()

        await self._validate_lead(data.lead_id)

        if project.lead_id == data.lead_id:
            return project

        try:
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

            updated = await self.repository.update_project(
                project,
                {"lead_id": data.lead_id},
            )

            await self.db.commit()
            await self.db.refresh(updated)

            return updated

        except Exception:
            await self.db.rollback()
            raise

    async def delete_project(
        self,
        project_id: int,
        current_user: EmployeeData,
    ) -> dict[str, str | int]:
        self._require_admin(current_user)

        project = await self.repository.get_project_by_id(
            project_id
        )
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
