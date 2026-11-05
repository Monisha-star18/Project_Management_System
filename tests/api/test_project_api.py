
from datetime import date

from app.core.security import hash_password
from app.models.employee import EmployeeData


def project_data(lead_id):
    return {
        "project_name": "Test Project",
        "project_description": "Project for API testing",
        "lead_id": lead_id,
        "start_date": "2026-11-10",
        "expected_end_date": "2026-12-10",
    }


async def create_project(client, auth_headers, admin):
    response = await client.post(
        "/api/projects/",
        json=project_data(admin.employee_id),
        headers=auth_headers,
    )

    assert response.status_code == 201
    return response.json()["project_id"]



# 1. CREATE PROJECT - VALID
async def test_create_project_valid(client, auth_headers, admin):

    response = await client.post(
        "/api/projects/",
        json=project_data(admin.employee_id),
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["project_name"] == "Test Project"


# 2. CREATE PROJECT - INVALID
async def test_create_project_invalid(client, auth_headers, admin):

    data = project_data(admin.employee_id)
    data["expected_end_date"] = "2026-11-12"

    response = await client.post(
        "/api/projects/",
        json=data,
        headers=auth_headers,
    )

    assert response.status_code == 422


# 3. GET ALL PROJECTS - VALID
async def test_get_all_projects_valid(client, auth_headers):

    response = await client.get(
        "/api/projects/?page=1&size=10",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 4. GET ALL PROJECTS - INVALID
async def test_get_all_projects_invalid(client, auth_headers):

    response = await client.get(
        "/api/projects/?page=0",
        headers=auth_headers,
    )

    assert response.status_code == 422


# 5. GET PROJECT BY ID - VALID
async def test_get_project_valid(client, auth_headers, admin):

    project_id = await create_project(client, auth_headers, admin)

    response = await client.get(
        f"/api/projects/{project_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == project_id


# 6. GET PROJECT BY ID - INVALID
async def test_get_project_invalid(client, auth_headers):

    response = await client.get(
        "/api/projects/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404


# 7. UPDATE PROJECT - VALID
async def test_update_project_valid(client, auth_headers, admin):

    project_id = await create_project(client, auth_headers, admin)

    response = await client.patch(
        f"/api/projects/{project_id}",
        json={"project_name": "Updated Project"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["project_name"] == "Updated Project"


# 8. UPDATE PROJECT - INVALID
async def test_update_project_invalid(client, auth_headers, admin):

    project_id = await create_project(client, auth_headers, admin)

    response = await client.patch(
        f"/api/projects/{project_id}",
        json={"expected_end_date": "2026-11-11"},
        headers=auth_headers,
    )

    assert response.status_code == 422


# 9. CHANGE PROJECT LEAD - VALID
async def test_change_project_lead_valid(
    client, auth_headers, admin, test_session
):

    project_id = await create_project(client, auth_headers, admin)

    new_lead = EmployeeData(
        full_name="New Team Lead",
        email="lead@test.com",
        phone="9876543211",
        department="IT",
        role="team_lead",
        password_hash=hash_password("Lead@123"),
        joining_date=date(2026, 1, 1),
        is_active=True,
    )

    test_session.add(new_lead)
    await test_session.commit()
    await test_session.refresh(new_lead)

    response = await client.patch(
        f"/api/projects/{project_id}/lead",
        json={
            "lead_id": new_lead.employee_id,
            "remark_on_remove": "Changing project lead",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["lead_id"] == new_lead.employee_id


# 10. CHANGE PROJECT LEAD - INVALID
async def test_change_project_lead_invalid(
    client, auth_headers, admin
):

    project_id = await create_project(client, auth_headers, admin)

    response = await client.patch(
        f"/api/projects/{project_id}/lead",
        json={
            "lead_id": 0,
            "remark_on_remove": "Invalid lead change",
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


# 11. DELETE PROJECT - VALID
async def test_delete_project_valid(client, auth_headers, admin):

    project_id = await create_project(client, auth_headers, admin)

    response = await client.delete(
        f"/api/projects/{project_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == project_id


# 12. DELETE PROJECT - INVALID
async def test_delete_project_invalid(client, auth_headers):

    response = await client.delete(
        "/api/projects/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404
