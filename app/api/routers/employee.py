
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependency.employee import get_employee_service
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
    status_code=status.HTTP_201_CREATED
)
async def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService=Depends(get_employee_service) ) -> EmployeeData:

    try:
        return await service.create_employee(employee)

    except EmployeeAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        ) from exc
