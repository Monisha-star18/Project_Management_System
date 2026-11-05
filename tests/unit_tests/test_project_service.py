from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.auth_exception import PermissionDeniedError
from app.exceptions.project_exception import (
    InvalidProjectUpdateError, ProjectAlreadyExistsError, ProjectNotFoundError,
)
from app.schemas.project import ProjectCreate, ProjectLeadUpdate, ProjectUpdate
from app.services.project_service import ProjectService


@pytest.fixture
def svc():
    repo, employee_repo, db = AsyncMock(), AsyncMock(), AsyncMock()
    return ProjectService(repo, employee_repo, db), repo, employee_repo, db


@pytest.fixture
def project():
    return SimpleNamespace(project_id=1010, lead_id=101, start_date=date(2026, 1, 1),
                           expected_end_date=date(2026, 1, 20), project_name="Website")


@pytest.fixture
def lead():
    return SimpleNamespace(employee_id=101, is_active=True, role="team_lead")


async def test_create_project_commits(svc, lead, project):
    service, repo, _, db = svc
    repo.create_new_project.return_value = project
    data = ProjectCreate(project_name="Website", lead_id=101,
                         start_date="2026-01-01", expected_end_date="2026-01-20")

    result = await service.create_project(data, lead)

    assert result.project_id == 1010
    repo.create_new_project.assert_awaited_once_with(data, 101)
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(project)


async def test_duplicate_project_rolls_back(svc, lead):
    service, repo, _, db = svc
    repo.create_new_project.side_effect = IntegrityError("x", {}, Exception())
    data = ProjectCreate(project_name="Website", lead_id=101,
                         start_date="2026-01-01", expected_end_date="2026-01-20")

    with pytest.raises(ProjectAlreadyExistsError):
        await service.create_project(data, lead)

    db.rollback.assert_awaited_once()


async def test_get_project_not_found(svc):
    service, repo, _, _ = svc
    repo.get_project_by_id.return_value = None

    with pytest.raises(ProjectNotFoundError):
        await service.get_project_by_id(999)


async def test_get_project_success(svc, project):
    service, repo, _, _ = svc
    repo.get_project_by_id.return_value = project
    assert await service.get_project_by_id(1010) is project


async def test_get_all_projects(svc):
    service, repo, _, _ = svc
    repo.get_all_projects.return_value = ["project"]
    assert await service.get_all_projects(1, 10) == ["project"]
    repo.get_all_projects.assert_awaited_once_with(1, 10)


async def test_update_project_commits(svc, project, lead):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project
    repo.update_project.return_value = project

    result = await service.update_project(1010, ProjectUpdate(project_name="New Website"), lead)

    assert result is project
    repo.update_project.assert_awaited_once_with(project, {"project_name": "New Website"})
    db.commit.assert_awaited_once()


async def test_update_project_denied_for_wrong_lead(svc, project):
    service, repo, _, _ = svc
    repo.get_project_by_id.return_value = project
    other_user = SimpleNamespace(employee_id=202, is_active=True)

    with pytest.raises(PermissionDeniedError):
        await service.update_project(1010, ProjectUpdate(status="started"), other_user)


async def test_update_project_short_duration(svc, project, lead):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project

    with pytest.raises(InvalidProjectUpdateError):
        await service.update_project(1010, ProjectUpdate(expected_end_date=date(2026, 1, 5)), lead)

    db.commit.assert_not_awaited()


async def test_update_project_duplicate_rolls_back(svc, project, lead):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project
    repo.update_project.side_effect = IntegrityError("x", {}, Exception())

    with pytest.raises(ProjectAlreadyExistsError):
        await service.update_project(1010, ProjectUpdate(project_name="Taken Name"), lead)

    db.rollback.assert_awaited_once()


async def test_change_project_lead(svc, project):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project
    db.scalar.side_effect = [None, None]  # Neither lead has an existing allotment
    db.add = Mock()  # SQLAlchemy Session.add is synchronous
    repo.update_project.return_value = project

    await service.change_project_lead(
        1010, ProjectLeadUpdate(lead_id=202, remark_on_remove="Lead reassigned")
    )

    db.add.assert_called_once()
    db.flush.assert_awaited_once()
    repo.update_project.assert_awaited_once_with(project, {"lead_id": 202})
    db.commit.assert_awaited_once()


async def test_delete_project(svc, project):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project

    result = await service.delete_project(1010)

    assert result["project_id"] == 1010
    repo.delete_project.assert_awaited_once_with(project)
    db.commit.assert_awaited_once()


async def test_delete_project_failure_rolls_back(svc, project):
    service, repo, _, db = svc
    repo.get_project_by_id.return_value = project
    repo.delete_project.side_effect = RuntimeError("database error")

    with pytest.raises(RuntimeError):
        await service.delete_project(1010)

    db.rollback.assert_awaited_once()
