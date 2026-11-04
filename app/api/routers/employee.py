from fastapi import APIRouter, Depends, Path, Query, status

from app.api.dependency.auth import require_roles
from app.api.dependency.employee_dependency import get_employee_service
from app.models.employee import EmployeeData
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeDetailsResponse,
    EmployeeUpdate,
    PaginatedEmployeeResponse,
)
from app.services.employee_service import EmployeeService

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)

dependAdmin = [Depends(require_roles("admin"))]

dependAll = [Depends(require_roles("admin", "employee", "team_lead"))]


#ADD EMPLOYEE DETAILS
@router.post(
    "/registration",
    response_model=EmployeeDetailsResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=dependAdmin,
    summary="Create a new Employee",
    description="Create a new Employee for the Company to work on the Projects ",
)
async def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService=Depends(get_employee_service)
) -> EmployeeData:

    return await service.create_employee(employee)


# GET ALL EMPLOYEES WITH PAGINATION
@router.get(
    "/",
    response_model=PaginatedEmployeeResponse,
    dependencies=dependAll,
    summary="Get all employees with pagination"
)
async def get_all_employees(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    service: EmployeeService = Depends(get_employee_service)
)->dict:
    return await service.get_all_employees(page, size)


# GET EMPLOYEE BY ID
@router.get(
    "/{employee_id}",
    response_model=EmployeeDetailsResponse,
    dependencies=dependAll,
    summary="Get employee by ID"
)
async def get_employee_by_id(
    employee_id: int = Path(..., gt=0),
    service: EmployeeService = Depends(get_employee_service)
)->EmployeeData:
    return await service.get_employee_by_id(employee_id)


# UPDATE EMPLOYEE DETAILS
@router.patch(
    "/{employee_id}",
    response_model=EmployeeDetailsResponse,
    dependencies=dependAdmin,
    summary="Update employee details"
)
async def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service)
)-> EmployeeData:
    return await service.update_employee(employee_id, employee)


# SOFT DELETE EMPLOYEE
@router.delete(
    "/{employee_id}",
    dependencies=dependAdmin,
    summary="Soft delete employee"
)
async def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service)
)-> dict:
    return await service.delete_employee(employee_id)

  