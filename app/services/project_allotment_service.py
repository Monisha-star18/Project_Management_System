from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.auth_exception import PermissionDeniedError
from app.exceptions.employee_exception import EmployeeNotFoundError
from app.exceptions.project_allotment_exception import (
    AllotmentConflictError,
    AllotmentNotFoundError,
    InvalidAllotmentEmployeeError,
    ProjectAllotmentAccessDeniedError,
    ProjectAllotmentNotFoundError,
)
from app.models.employee import EmployeeData
from app.models.project import ProjectDetails
from app.models.project_allotment import ProjectAllotment
from app.repositories.interfaces.employee_repository_interface import (
    EmployeeRepositoryInterface,
)
from app.repositories.interfaces.project_allotment_repository_interface import (
    ProjectAllotmentRepositoryInterface,
)
from app.schemas.project_allotment import (
    AllotmentCreate,
    AllotmentListResponse,
    AllotmentResponse,
)


class ProjectAllotmentService:
    def __init__(
        self,
        repository: ProjectAllotmentRepositoryInterface,
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

        if project.lead_id != current_user.employee_id:
            raise ProjectAllotmentAccessDeniedError()
        
        
    async def add_employee(
        self, 
        project_id: int, 
        data: AllotmentCreate, 
        current_user: EmployeeData
    ) -> AllotmentResponse:
        
        project = await self.repository.get_project_with_members(project_id)
        
        if project is None:
            raise ProjectAllotmentNotFoundError()

        self._check_project_lead(current_user, project)
        
        employee = await self.employee_repository.get_employee_by_id(data.employee_id)
        
        if (
            employee is None
            or not employee.is_active
            or employee.role == "admin"
        ):
            raise InvalidAllotmentEmployeeError()

        existing = await self.repository.get_membership(project_id, data.employee_id)
        
        if existing is not None:
            raise AllotmentConflictError()

        try:
            if existing is not None:
                allotment = existing
                allotment.is_active = True
                allotment.remark_on_remove = None
            else:
                allotment = await self.repository.add_member(
                    project_id, data.employee_id
                )
                
            await self.db.commit()
            await self.db.refresh(allotment)
        
        except IntegrityError as exc:
           
            await self.db.rollback()
            # Only report a membership conflict for this unique constraint.
            diag = getattr(getattr(exc, "orig", None), "diag", None)
            constraint_name = getattr(diag, "constraint_name", None)
            if constraint_name == "uq_project_employee":
                raise AllotmentConflictError() from exc
            raise
        
        except Exception:
            await self.db.rollback()
            raise

        # No lazy loading: the employee was explicitly fetched above.
        return AllotmentResponse(
                allotment_id=allotment.allotment_id,
                project_id=allotment.project_id,
                employee_id=allotment.employee_id,
                employee_name=employee.full_name,
                role=employee.role,
        )

    async def list_members(
        self,
        project_id: int,
    ) -> AllotmentListResponse:

        project = await self.repository.get_project_with_members(project_id)

        if project is None:
            raise ProjectAllotmentNotFoundError()

        members = [
            allotment
            for allotment in project.allotments
            if allotment.is_active
        ]

        return AllotmentListResponse(
            project_id=project_id,
            total=len(members),
            members=[
                AllotmentResponse(
                    allotment_id=allotment.allotment_id,
                    project_id=allotment.project_id,
                    employee_id=allotment.employee_id,
                    employee_name=allotment.employee.full_name,
                    role=allotment.employee.role,
                )
                for allotment in members
            ]
        )

    async def remove_employee(
        self, 
        project_id: int, 
        employee_id: int, 
        current_user: EmployeeData
    ) -> dict[str, str | int]:
        
        project = await self.repository.get_project_with_members(project_id)
       
        if project is None:
            raise ProjectAllotmentNotFoundError()

        self._check_project_lead(current_user, project)
            
        if employee_id == project.lead_id:
            raise AllotmentConflictError("Current project lead cannot be removed")

        allotment = await self.repository.get_membership(project_id, employee_id)
        
        if allotment is None:
            raise AllotmentNotFoundError()

        try:
            await self.repository.remove_member(allotment)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return {"message": "Employee removed and their project tasks deleted", 
                "employee_id": employee_id
                }

        
    async def get_employee_allotments(
        self,
        employee_id: int,
    ) -> list[ProjectAllotment]:

       
        employee = await self.employee_repository.get_employee_by_id(employee_id)

        if employee is None:
            raise EmployeeNotFoundError()

        allotments = await self.repository.get_employee_allotments(employee_id)

        return [
            AllotmentResponse(
                allotment_id=allotment.allotment_id,
                project_id=allotment.project_id,
                employee_id=allotment.employee_id,
                employee_name=employee.full_name,
                role=employee.role,
            )
            for allotment in allotments
        ]

