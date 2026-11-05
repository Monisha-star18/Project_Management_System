
import pytest


VALID_EMPLOYEE = {
    "full_name": "Ravi Kumar",
    "email": "ravi@test.com",
    "phone": "9123456789",
    "department": "IT",
    "password": "Passw0rd@1",
    "joining_date": "2026-01-01",
}


# Helper to create an employee for other tests
async def create_employee(client, auth_headers):
    response = await client.post(
        "/api/employees/registration",
        json=VALID_EMPLOYEE,
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["employee_id"]


# 1. CREATE EMPLOYEE - VALID
async def test_create_employee_valid(client, auth_headers):

    response = await client.post(
        "/api/employees/registration",
        json=VALID_EMPLOYEE,
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json()["full_name"] == "Ravi Kumar"


# 2. CREATE EMPLOYEE - INVALID
async def test_create_employee_invalid(client, auth_headers):

    data = {**VALID_EMPLOYEE, "email": "invalid-email"}

    response = await client.post(
        "/api/employees/registration",
        json=data,
        headers=auth_headers
    )

    assert response.status_code == 422


# 3. GET ALL EMPLOYEES - VALID
async def test_get_all_employees_valid(client, auth_headers):

    response = await client.get(
        "/api/employees/?page=1&size=10",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert "employees" in response.json()


# 4. GET ALL EMPLOYEES - INVALID
async def test_get_all_employees_invalid(client, auth_headers):

    response = await client.get(
        "/api/employees/?page=0",
        headers=auth_headers
    )

    assert response.status_code == 422


# 5. GET EMPLOYEE BY ID - VALID
async def test_get_employee_valid(client, auth_headers):

    employee_id = await create_employee(client, auth_headers)

    response = await client.get(
        f"/api/employees/{employee_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_id


# 6. GET EMPLOYEE BY ID - INVALID
async def test_get_employee_invalid(client, auth_headers):

    response = await client.get(
        "/api/employees/99999",
        headers=auth_headers
    )

    assert response.status_code == 404


# 7. UPDATE EMPLOYEE - VALID
async def test_update_employee_valid(client, auth_headers):

    employee_id = await create_employee(client, auth_headers)

    response = await client.patch(
        f"/api/employees/{employee_id}",
        json={"full_name": "Ravi Updated"},
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Ravi Updated"


# 8. UPDATE EMPLOYEE - INVALID
async def test_update_employee_invalid(client, auth_headers):

    employee_id = await create_employee(client, auth_headers)

    response = await client.patch(
        f"/api/employees/{employee_id}",
        json={"full_name": None},
        headers=auth_headers
    )

    assert response.status_code == 422


# 9. DELETE EMPLOYEE - VALID
async def test_delete_employee_valid(client, auth_headers):

    employee_id = await create_employee(client, auth_headers)

    response = await client.delete(
        f"/api/employees/{employee_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == employee_id


# 10. DELETE EMPLOYEE - INVALID
async def test_delete_employee_invalid(client, auth_headers):

    response = await client.delete(
        "/api/employees/99999",
        headers=auth_headers
    )

    assert response.status_code == 404
