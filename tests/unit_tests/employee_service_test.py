from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.employee_exception import (
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    InvalidEmployeeUpdateError,
)
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import EmployeeService

VALID_EMPLOYEE = dict(
    full_name="Ravi Kumar", email="ravi@test.com", phone="9876543210",
    department="IT", password="Passw0rd@1", joining_date="2026-01-01",
)


@pytest.fixture
def svc():
    repo, db = AsyncMock(), AsyncMock()
    return EmployeeService(repo, db) , repo, db


async def test_create_employee_commits(svc):
    service, repo, db = svc
    
    repo.create_new_employee.return_value = SimpleNamespace(employee_id=101)

    result = await service.create_employee(
        EmployeeCreate(**VALID_EMPLOYEE)
        )
    
    assert result.employee_id == 101

    db.commit.assert_awaited_once()


async def test_create_duplicate_employee_rolls_back(svc):
    service, repo, db = svc
    
    repo.create_new_employee.side_effect = IntegrityError("x", {}, Exception())

    with pytest.raises(EmployeeAlreadyExistsError):
        await service.create_employee(EmployeeCreate(**VALID_EMPLOYEE))

    db.rollback.assert_awaited_once()


async def test_get_employee_not_found(svc):
    service, repo, _ = svc
   
    repo.get_employee_by_id.return_value = None
   
    with pytest.raises(EmployeeNotFoundError):
        await service.get_employee_by_id(999)


async def test_update_with_null_value_rejected(svc):
    
    service, repo, _ = svc
    
    repo.get_employee_by_id.return_value = SimpleNamespace()
    with pytest.raises(InvalidEmployeeUpdateError):
        await service.update_employee(101, EmployeeUpdate(full_name=None))


async def test_pagination_page_count(svc):
    
    service, repo, _ = svc
    
    repo.get_all_employees.return_value = ([], 25)
    assert (await service.get_all_employees(page=1, size=10))["pages"] == 3


async def test_delete_employee(svc):
   
    service, repo, db = svc
   
    repo.get_employee_by_id.return_value = SimpleNamespace()
   
    result = await service.delete_employee(101)
   
    assert result["employee_id"] == 101
   
    repo.soft_delete_employee.assert_awaited_once()
    db.commit.assert_awaited_once()
