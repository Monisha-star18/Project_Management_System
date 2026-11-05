
from datetime import date

from app.models.employee import EmployeeData
from app.core.security import hash_password, create_access_token


# Create project and allot employee
async def setup_project(
    client, auth_headers, lead_headers, team_lead, test_session
):
    response = await client.post(
        "/api/projects/",
        json={
            "project_name": "Task Test Project",
            "project_description": "API testing",
            "lead_id": team_lead.employee_id,
            "start_date": "2026-11-10",
            "expected_end_date": "2026-12-10",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    project_id = response.json()["project_id"]

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

    response = await client.post(
        f"/api/projects/{project_id}/allotments",
        json={"employee_id": employee.employee_id},
        headers=lead_headers,
    )

    assert response.status_code == 201

    employee_headers = {
        "Authorization": (
            f"Bearer {create_access_token(employee.email)}"
        )
    }

    return project_id, employee.employee_id, employee_headers


# Task data
def task_data(employee_id):
    return {
        "employee_id": employee_id,
        "task_title": "Develop Login API",
        "description": "Implement authentication",
        "priority": "high",
        "start_date": "2026-11-11",
        "due_date": "2026-11-20",
    }


# Create task for other tests
async def setup_task(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, employee_id, employee_headers = await setup_project(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.post(
        f"/api/projects/{project_id}/tasks",
        json=task_data(employee_id),
        headers=lead_headers,
    )

    assert response.status_code == 201

    return (
        project_id,
        employee_id,
        response.json()["task_id"],
        employee_headers,
    )



# 1. CREATE TASK - VALID
async def test_create_task_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, employee_id, _ = await setup_project(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.post(
        f"/api/projects/{project_id}/tasks",
        json=task_data(employee_id),
        headers=lead_headers,
    )

    assert response.status_code == 201
    assert response.json()["task_title"] == "Develop Login API"


# 2. CREATE TASK - INVALID
async def test_create_task_invalid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, employee_id, _ = await setup_project(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    data = task_data(employee_id)
    data["due_date"] = "2026-11-01"

    response = await client.post(
        f"/api/projects/{project_id}/tasks",
        json=data,
        headers=lead_headers,
    )

    assert response.status_code == 422


# 3. LIST PROJECT TASKS - VALID
async def test_list_project_tasks_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, _, _, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.get(
        f"/api/projects/{project_id}/tasks",
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 4. LIST PROJECT TASKS - INVALID
async def test_list_project_tasks_invalid(client, lead_headers):

    response = await client.get(
        "/api/projects/99999/tasks",
        headers=lead_headers,
    )

    assert response.status_code == 404


# 5. GET TASK - VALID
async def test_get_task_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.get(
        f"/api/tasks/{task_id}",
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert response.json()["task_id"] == task_id


# 6. GET TASK - INVALID
async def test_get_task_invalid(client, lead_headers):

    response = await client.get(
        "/api/tasks/99999",
        headers=lead_headers,
    )

    assert response.status_code == 404


# 7. GET MY TASKS - VALID
async def test_get_my_tasks_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, employee_headers = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.get(
        "/api/employees/me/tasks",
        headers=employee_headers,
    )

    assert response.status_code == 200
    assert response.json()[0]["task_id"] == task_id


# 8. GET MY TASKS - INVALID
async def test_get_my_tasks_invalid(client, auth_headers):

    response = await client.get(
        "/api/employees/me/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 403


# 9. GET EMPLOYEE PROJECT TASKS - VALID
async def test_employee_project_tasks_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, employee_id, _, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.get(
        f"/api/projects/{project_id}/employees/{employee_id}/tasks",
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 10. GET EMPLOYEE PROJECT TASKS - INVALID
async def test_employee_project_tasks_invalid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    project_id, _, _ = await setup_project(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.get(
        f"/api/projects/{project_id}/employees/0/tasks",
        headers=lead_headers,
    )

    assert response.status_code == 422


# 11. UPDATE TASK - VALID
async def test_update_task_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.patch(
        f"/api/tasks/{task_id}",
        json={"task_title": "Updated Login API"},
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert response.json()["task_title"] == "Updated Login API"


# 12. UPDATE TASK - INVALID
async def test_update_task_invalid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.patch(
        f"/api/tasks/{task_id}",
        json={"task_title": None},
        headers=lead_headers,
    )

    assert response.status_code == 422


# 13. UPDATE TASK PROGRESS - VALID
async def test_update_progress_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, employee_headers = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.patch(
        f"/api/tasks/{task_id}/progress",
        json={"progress_percentage": 50},
        headers=employee_headers,
    )

    assert response.status_code == 200
    assert response.json()["progress_percentage"] == 50
    assert response.json()["status"] == "in_progress"


# 14. UPDATE TASK PROGRESS - INVALID
async def test_update_progress_invalid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, employee_headers = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.patch(
        f"/api/tasks/{task_id}/progress",
        json={"progress_percentage": 110},
        headers=employee_headers,
    )

    assert response.status_code == 422


# 15. DELETE TASK - VALID
async def test_delete_task_valid(
    client, auth_headers, lead_headers, team_lead, test_session
):
    _, _, task_id, _ = await setup_task(
        client, auth_headers, lead_headers, team_lead, test_session
    )

    response = await client.delete(
        f"/api/tasks/{task_id}",
        headers=lead_headers,
    )

    assert response.status_code == 200
    assert response.json()["task_id"] == task_id


# 16. DELETE TASK - INVALID
async def test_delete_task_invalid(client, lead_headers):

    response = await client.delete(
        "/api/tasks/99999",
        headers=lead_headers,
    )

    assert response.status_code == 404
