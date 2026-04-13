def register_user(client, email, password="secret123"):
    response = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 201, response.text
    return response.json()["user_id"]


def create_project(client, created_by, name="Project A"):
    response = client.post(
        "/projects/",
        json={"created_by": created_by, "name": name},
    )
    assert response.status_code == 200, response.text
    return response.json()


def create_column(client, project_id, name="To Do", position=1):
    response = client.post(
        "/columns/",
        json={"project_id": project_id, "name": name, "position": position},
    )
    assert response.status_code == 200, response.text
    return response.json()


def create_task(
    client,
    column_id,
    created_by,
    assigned_to,
    title="Task A",
    description="Initial description",
    is_finished=False,
):
    response = client.post(
        "/tasks/",
        json={
            "column_id": column_id,
            "created_by": created_by,
            "assigned_to": assigned_to,
            "title": title,
            "description": description,
            "is_finished": is_finished,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()
