from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.exceptions.auth_exception import PermissionDeniedError
from app.exceptions.project_exception import ProjectNotFoundError
from app.exceptions.task_exception import (
    InvalidTaskUpdateError,
    TaskAssignmentError,
    TaskNotFoundError,
)
from app.schemas.task import TaskCreate, TaskProgressUpdate, TaskUpdate
from app.services.task_service import TaskService


@pytest.fixture
def svc():
    repo, db = AsyncMock(), AsyncMock()
    return TaskService(repo, db), repo, db


@pytest.fixture
def lead():
    return SimpleNamespace(employee_id=101, role="team_lead")


@pytest.fixture
def employee():
    return SimpleNamespace(employee_id=202, role="employee")


@pytest.fixture
def project():
    return SimpleNamespace(project_id=1010, lead_id=101)


@pytest.fixture
def task():
    allotment = SimpleNamespace(allotment_id=5, project_id=1010, employee_id=202, is_active=True)
    return SimpleNamespace(task_id=10, allotment_id=5, allotment=allotment,
                           task_title="Write tests", description=None, assigned_by=101,
                           priority="medium", start_date=date(2026, 1, 1),
                           due_date=date(2026, 1, 10), status="todo", progress_percentage=0,
                           remarks=None, created_at=datetime(2026, 1, 1),
                           updated_at=datetime(2026, 1, 1))


async def test_create_task_commits(svc, lead, project, task):
    service, repo, db = svc
    repo.get_project.return_value = project
    repo.get_allotment.return_value = task.allotment
    repo.get_task.return_value = task

    async def assign_id(new_task):
        new_task.task_id = 10  # Simulate DB-generated ID

    repo.add_task.side_effect = assign_id
    data = TaskCreate(employee_id=202, task_title="Write tests",
                      start_date="2026-01-01", due_date="2026-01-10")

    result = await service.create(1010, data, lead)

    assert result.task_id == 10
    repo.add_task.assert_awaited_once()
    db.commit.assert_awaited_once()


async def test_create_project_missing(svc, lead):
    service, repo, _ = svc
    repo.get_project.return_value = None
    data = TaskCreate(employee_id=202, task_title="Write tests",
                      start_date="2026-01-01", due_date="2026-01-10")

    with pytest.raises(ProjectNotFoundError):
        await service.create(999, data, lead)


async def test_create_denied_for_non_lead(svc, employee, project):
    service, repo, _ = svc
    repo.get_project.return_value = project
    data = TaskCreate(employee_id=202, task_title="Write tests",
                      start_date="2026-01-01", due_date="2026-01-10")

    with pytest.raises(PermissionDeniedError):
        await service.create(1010, data, employee)


async def test_create_unallotted_employee(svc, lead, project):
    service, repo, _ = svc
    repo.get_project.return_value = project
    repo.get_allotment.return_value = None
    data = TaskCreate(employee_id=202, task_title="Write tests",
                      start_date="2026-01-01", due_date="2026-01-10")

    with pytest.raises(TaskAssignmentError):
        await service.create(1010, data, lead)


async def test_list_project_tasks(svc, lead, project, task):
    service, repo, _ = svc
    repo.get_project.return_value = project
    repo.list_tasks.return_value = [task]

    result = await service.list_project(1010, lead)

    assert len(result) == 1
    assert result[0].task_title == "Write tests"
    repo.list_tasks.assert_awaited_once_with(project_id=1010)


async def test_get_task_not_found(svc, lead):
    service, repo, _ = svc
    repo.get_task.return_value = None

    with pytest.raises(TaskNotFoundError):
        await service.get(999, lead)


async def test_get_task_by_assigned_employee(svc, employee, project, task):
    service, repo, _ = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project

    result = await service.get(10, employee)

    assert result.task_id == 10


async def test_get_task_denied_for_other_employee(svc, project, task):
    service, repo, _ = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project
    other_employee = SimpleNamespace(employee_id=303, role="employee")

    with pytest.raises(PermissionDeniedError):
        await service.get(10, other_employee)


async def test_mine_excludes_inactive_memberships(svc, employee, task):
    service, repo, _ = svc
    inactive = SimpleNamespace(allotment=SimpleNamespace(is_active=False))
    repo.list_tasks.return_value = [task, inactive]

    result = await service.mine(employee)

    assert len(result) == 1
    assert result[0].task_id == 10


async def test_project_employee_tasks(svc, lead, project, task):
    service, repo, _ = svc
    repo.get_project.return_value = project
    repo.list_tasks.return_value = [task]

    result = await service.project_employee(1010, 202, lead)

    assert len(result) == 1
    repo.list_tasks.assert_awaited_once_with(project_id=1010, employee_id=202)


async def test_project_employee_denied_for_other_employee(svc, employee, project):
    service, repo, _ = svc
    repo.get_project.return_value = project

    with pytest.raises(PermissionDeniedError):
        await service.project_employee(1010, 303, employee)


async def test_update_task_commits(svc, lead, project, task):
    service, repo, db = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project

    result = await service.update(10, TaskUpdate(task_title="Updated title"), lead)

    assert result.task_title == "Updated title"
    db.commit.assert_awaited_once()


async def test_update_task_null_rejected(svc, lead, project, task):
    service, repo, _ = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project

    with pytest.raises(InvalidTaskUpdateError):
        await service.update(10, TaskUpdate(task_title=None), lead)


async def test_update_task_invalid_dates(svc, lead, project, task):
    service, repo, _ = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project

    with pytest.raises(InvalidTaskUpdateError):
        await service.update(10, TaskUpdate(due_date=date(2025, 12, 31)), lead)


async def test_update_task_reassign(svc, lead, project, task):
    service, repo, db = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project
    repo.get_allotment.return_value = SimpleNamespace(allotment_id=8)

    await service.update(10, TaskUpdate(employee_id=303), lead)

    assert task.allotment_id == 8
    repo.get_allotment.assert_awaited_once_with(1010, 303)
    db.commit.assert_awaited_once()


async def test_progress_100_completes_task(svc, employee, task):
    service, repo, db = svc
    repo.get_task.return_value = task

    result = await service.progress(10, TaskProgressUpdate(progress_percentage=100), employee)

    assert result.status == "completed"
    assert result.progress_percentage == 100
    db.commit.assert_awaited_once()


async def test_progress_denied_to_other_employee(svc, task):
    service, repo, _ = svc
    repo.get_task.return_value = task
    other = SimpleNamespace(employee_id=303, role="employee")

    with pytest.raises(PermissionDeniedError):
        await service.progress(10, TaskProgressUpdate(progress_percentage=50), other)


async def test_progress_50_sets_in_progress(svc, employee, task):
    service, repo, _ = svc
    repo.get_task.return_value = task

    result = await service.progress(10, TaskProgressUpdate(progress_percentage=50), employee)

    assert result.status == "in_progress"


async def test_delete_task_commits(svc, lead, project, task):
    service, repo, db = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project

    result = await service.delete(10, lead)

    assert result["task_id"] == 10
    repo.delete_task.assert_awaited_once_with(task)
    db.commit.assert_awaited_once()


async def test_delete_task_failure_rolls_back(svc, lead, project, task):
    service, repo, db = svc
    repo.get_task.return_value = task
    repo.get_project.return_value = project
    repo.delete_task.side_effect = RuntimeError("database error")

    with pytest.raises(RuntimeError):
        await service.delete(10, lead)

    db.rollback.assert_awaited_once()
