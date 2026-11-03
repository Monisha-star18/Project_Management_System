from fastapi import APIRouter, Depends, status
from app.api.dependency.auth import require_roles
from app.api.dependency.employee_dependency import get_employee_service
from app.exceptions.employee_exception import EmployeeAlreadyExistsError
from app.models.employee import EmployeeData
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.services.employee_service import EmployeeService


router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[ Depends(require_roles("admin")) ],
    summary="Create a new Employee",
    description="Create a new Employee for the Company to work on the Projects ",
)
async def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService=Depends(get_employee_service) ) -> EmployeeData:

    return await service.create_employee(employee)

  