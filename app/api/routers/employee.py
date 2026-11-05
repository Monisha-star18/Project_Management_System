from typing import Annotated

from fastapi import APIRouter,BackgroundTasks, Depends, Path, Query, status

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
from app.services.email.employee_created_email import EmployeeCreatedEmail

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
    description="Admin only. Register a new employee with their personal details, email, password and assigned role. Sends a registration notification email to the newly created employee."
)
async def create_employee(
    employee: EmployeeCreate,
    background_tasks: BackgroundTasks,
    service: EmployeeService=Depends(get_employee_service)
) -> EmployeeData:

    new_employee = await service.create_employee(employee)

    email_service = EmployeeCreatedEmail()

    background_tasks.add_task(
        email_service.send,
        new_employee.email,
        new_employee.full_name,
    )

    return new_employee


# GET ALL EMPLOYEES WITH PAGINATION
@router.get(
    "/",
    response_model=PaginatedEmployeeResponse,
    dependencies=dependAll,
    summary="Get all employees with pagination",
    description="Retrieve a paginated list of registered employees. Accessible to admins, team leads and employees. Supports page and size query parameters."
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
    summary="Get employee by ID",
    description="Retrieve the details of a specific employee using their employee ID. Accessible to authenticated admins, team leads and employees."
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
    summary="Update employee details",
    description="Admin only. Update an existing employee's details using their employee ID. Only the fields provided in the request are updated."
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
    summary="Soft delete employee",
    description="Admin only. Soft delete an employee by marking their account as inactive without permanently removing their record from the database."
)
async def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service)
)-> dict:
    return await service.delete_employee(employee_id)

  