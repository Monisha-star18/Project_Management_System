async def test_health_api(client):

    response = await client.get("/api/health/")

    assert response.status_code == 200

    assert response.json()["status"] == "success"

async def test_database_connection(client):

    response = await client.get("/api/health/db")

    assert response.status_code == 200

    assert response.json()["message"] == (
        "Database connected successfully"
    )