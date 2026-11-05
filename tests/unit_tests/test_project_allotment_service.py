from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.employee_exception import EmployeeNotFoundError
from app.exceptions.project_allotment_exception import (
    AllotmentConflictError,
    AllotmentNotFoundError,
    InvalidAllotmentEmployeeError,
    ProjectAllotmentNotFoundError,
)
from app.schemas.project_allotment import AllotmentCreate
from app.services.project_allotment_service import ProjectAllotmentService


@pytest.fixture
def svc():
    repo, employee_repo, db = AsyncMock(), AsyncMock(), AsyncMock()
    return ProjectAllotmentService(repo, employee_repo, db), repo, employee_repo, db


@pytest.fixture
def employee():
    return SimpleNamespace(employee_id=101, full_name="Ravi Kumar", is_active=True, role="employee")


@pytest.fixture
def membership(employee):
    return SimpleNamespace(allotment_id=1, project_id=1010, employee_id=101,
                           is_active=True, employee=employee)


async def test_add_employee_commits(svc, employee, membership):
    service, repo, employee_repo, db = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    employee_repo.get_employee_by_id.return_value = employee
    repo.get_membership.return_value = None
    repo.add_member.return_value = membership

    result = await service.add_employee(1010, AllotmentCreate(employee_id=101), employee)

    assert result.employee_id == 101
    assert result.employee_name == "Ravi Kumar"
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(membership)


async def test_add_employee_project_not_found(svc, employee):
    service, repo, _, _ = svc
    repo.get_project_with_members.return_value = None

    with pytest.raises(ProjectAllotmentNotFoundError):
        await service.add_employee(999, AllotmentCreate(employee_id=101), employee)


async def test_add_inactive_employee_rejected(svc, employee):
    service, repo, employee_repo, _ = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    employee_repo.get_employee_by_id.return_value = SimpleNamespace(is_active=False, role="employee")

    with pytest.raises(InvalidAllotmentEmployeeError):
        await service.add_employee(1010, AllotmentCreate(employee_id=101), employee)


async def test_add_duplicate_membership(svc, employee, membership):
    service, repo, employee_repo, _ = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    employee_repo.get_employee_by_id.return_value = employee
    repo.get_membership.return_value = membership

    with pytest.raises(AllotmentConflictError):
        await service.add_employee(1010, AllotmentCreate(employee_id=101), employee)


async def test_add_database_error_rolls_back(svc, employee):
    service, repo, employee_repo, db = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    employee_repo.get_employee_by_id.return_value = employee
    repo.get_membership.return_value = None
    repo.add_member.side_effect = IntegrityError("x", {}, Exception())

    with pytest.raises(IntegrityError):
        await service.add_employee(1010, AllotmentCreate(employee_id=101), employee)

    db.rollback.assert_awaited_once()


async def test_list_members_excludes_inactive(svc, membership):
    service, repo, _, _ = svc
    inactive = SimpleNamespace(is_active=False)
    repo.get_project_with_members.return_value = SimpleNamespace(allotments=[membership, inactive])

    result = await service.list_members(1010)

    assert result.total == 1
    assert result.members[0].employee_id == 101


async def test_list_members_project_not_found(svc):
    service, repo, _, _ = svc
    repo.get_project_with_members.return_value = None

    with pytest.raises(ProjectAllotmentNotFoundError):
        await service.list_members(999)


async def test_remove_employee_commits(svc, employee, membership):
    service, repo, _, db = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    repo.get_membership.return_value = membership

    result = await service.remove_employee(1010, 101, employee)

    assert result["employee_id"] == 101
    repo.remove_member.assert_awaited_once_with(membership)
    db.commit.assert_awaited_once()


async def test_remove_project_lead_rejected(svc, employee):
    service, repo, _, db = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=101)

    with pytest.raises(AllotmentConflictError):
        await service.remove_employee(1010, 101, employee)

    db.commit.assert_not_awaited()


async def test_remove_membership_not_found(svc, employee):
    service, repo, _, _ = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    repo.get_membership.return_value = None

    with pytest.raises(AllotmentNotFoundError):
        await service.remove_employee(1010, 101, employee)


async def test_remove_failure_rolls_back(svc, employee, membership):
    service, repo, _, db = svc
    repo.get_project_with_members.return_value = SimpleNamespace(lead_id=202)
    repo.get_membership.return_value = membership
    repo.remove_member.side_effect = RuntimeError("database error")

    with pytest.raises(RuntimeError):
        await service.remove_employee(1010, 101, employee)

    db.rollback.assert_awaited_once()


async def test_get_employee_allotments(svc, employee, membership):
    service, repo, employee_repo, _ = svc
    employee_repo.get_employee_by_id.return_value = employee
    repo.get_employee_allotments.return_value = [membership]

    result = await service.get_employee_allotments(101)

    assert len(result) == 1
    assert result[0].project_id == 1010


async def test_get_allotments_employee_not_found(svc):
    service, _, employee_repo, _ = svc
    employee_repo.get_employee_by_id.return_value = None

    with pytest.raises(EmployeeNotFoundError):
        await service.get_employee_allotments(999)
