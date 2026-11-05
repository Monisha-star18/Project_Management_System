
# 1. LOGIN - VALID
async def test_login_valid(client, admin):

    response = await client.post(
        "/api/auth/login",
        data={
            "username": admin.email,
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


# 2. LOGIN - INVALID
async def test_login_invalid(client, admin):

    response = await client.post(
        "/api/auth/login",
        data={
            "username": admin.email,
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


# 3. GET CURRENT USER - VALID
async def test_get_me_valid(client, auth_headers, admin):

    response = await client.get(
        "/api/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["employee_id"] == admin.employee_id
    assert response.json()["email"] == admin.email


# 4. GET CURRENT USER - INVALID
async def test_get_me_invalid(client):

    response = await client.get(
        "/api/auth/me",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 401
