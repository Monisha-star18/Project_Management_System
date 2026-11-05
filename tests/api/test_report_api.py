
# Helper to create a project
async def create_project(client, auth_headers, team_lead):

    response = await client.post(
        "/api/projects/",
        json={
            "project_name": "Report Test Project",
            "project_description": "Project for report testing",
            "lead_id": team_lead.employee_id,
            "start_date": "2026-11-10",
            "expected_end_date": "2026-12-10",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201

    return response.json()["project_id"]

async def test_get_project_report_valid(
    client, auth_headers, team_lead
):

    project_id = await create_project(
        client, auth_headers, team_lead
    )

    response = await client.get(
        f"/api/reports/projects/{project_id}",
        headers=auth_headers,
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200
    

# 2. GET PROJECT REPORT - INVALID
async def test_get_project_report_invalid(client, auth_headers):

    response = await client.get(
        "/api/reports/projects/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404
