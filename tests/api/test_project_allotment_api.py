
from datetime import date

from app.models.employee import EmployeeData
from app.core.security import hash_password


# Create a project with our test team lead
async def create_project(client, auth_headers, team_lead):

    response = await client.post(
        "/api/projects/",
        json={
            "project_name": "Allotment Test Project",
            "project_description": "API testing",
            "lead_id": team_lead.employee_id,
            "start_date": "2026-11-10",
            "expected_end_date": "2026-12-10",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    return response.json()["project_id"]


# Create an employee in the test database
async def create_employee(test_session):

    employee = EmployeeData(
        full_name="Ravi Kumar",
        email="ravi@test.com",
        phone="9123456789",
        department="IT",
        role="employee",
        password_hash=hash_password("Passw0rd@1"),
        joining_date=date(2026, 1, 1),
        is_active=True,
    )

    test_session.add(employee)
    await test_session.commit()
    await test_session.refresh(employee)

    return employee.employee_id


# 1. ALLOT EMPLOYEE - VALID
async def test_allot_employee_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id = await create_project(client, auth_headers, team_lead)
    employee_id = await create_employee(test_session)

    response = await client.post(
        f"/api/projects/{project_id}/allotments",
        json={"employee_id": employee_id},
        headers=lead_headers,
    )

    assert response.status_code == 201
    assert response.json()["employee_id"] == employee_id


# 2. ALLOT EMPLOYEE - INVALID
async def test_allot_employee_invalid(
    client, auth_headers, lead_headers, team_lead
):
    project_id = await create_project(client, auth_headers, team_lead)

    response = await client.post(
        f"/api/projects/{project_id}/allotments",
        json={"employee_id": 0},
        headers=lead_headers,
    )

    assert response.status_code == 422


# 3. GET PROJECT ALLOTMENTS - VALID
async def test_get_project_allotments_valid(
    client, auth_headers, team_lead
):
    project_id = await create_project(client, auth_headers, team_lead)

    response = await client.get(
        f"/api/projects/{project_id}/allotments",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == project_id
    assert "members" in response.json()


# 4. GET PROJECT ALLOTMENTS - INVALID
async def test_get_project_allotments_invalid(client, auth_headers):

    response = await client.get(
        "/api/projects/99999/allotments",
        headers=auth_headers,
    )

    assert response.status_code == 404


# 5. GET EMPLOYEE ALLOTMENTS - VALID
async def test_get_employee_allotments_valid(
    client, auth_headers, test_session
):
    employee_id = await create_employee(test_session)

    response = await client.get(
        f"/api/projects/employees/{employee_id}/allotments",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 6. GET EMPLOYEE ALLOTMENTS - INVALID
async def test_get_employee_allotments_invalid(client, auth_headers):

    response = await client.get(
        "/api/projects/employees/99999/allotments",
        headers=auth_headers,
    )

    assert response.status_code == 404


# 7. REMOVE ALLOTMENT - VALID
async def test_remove_allotment_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id = await create_project(client, auth_headers, team_lead)
    employee_id = await create_employee(test_session)

    await client.post(
        f"/api/projects/{project_id}/allotments",
        json={"employee_id": employee_id},
        headers=lead_headers,
    )

    response = await client.delete(
        f"/api/projects/{project_id}/allotments/{employee_id}",
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_id


# 8. REMOVE ALLOTMENT - INVALID
async def test_remove_allotment_invalid(
    client, auth_headers, lead_headers, team_lead
):
    project_id = await create_project(client, auth_headers, team_lead)

    response = await client.delete(
        f"/api/projects/{project_id}/allotments/99999",
        headers=lead_headers,
    )

    assert response.status_code == 404
