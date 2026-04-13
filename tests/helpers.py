def register_user(client, email, password="secret123", first_name="Test", last_name="User"):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["user_id"]


def login_user(client, email, password="secret123"):
    response = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_project(client, headers, name="Project A"):
    # In some versions it might require created_by in JSON, 
    # but our endpoint overrides it with current_user.id
    response = client.post(
        "/projects/",
        json={"name": name, "created_by": 0}, # dummy created_by
        headers=headers
    )
    assert response.status_code == 200, response.text
    return response.json()


def create_column(client, headers, project_id, name="To Do", position=1):
    response = client.post(
        "/columns/",
        json={"project_id": project_id, "name": name, "position": position},
        headers=headers
    )
    assert response.status_code == 200, response.text
    return response.json()


def create_task(
    client,
    headers,
    column_id,
    assigned_to,
    title="Task A",
    description="Initial description",
    is_finished=False,
):
    response = client.post(
        "/tasks/",
        json={
            "column_id": column_id,
            "assigned_to": assigned_to,
            "title": title,
            "description": description,
            "is_finished": is_finished,
            "created_by": 0, # dummy
        },
        headers=headers
    )
    assert response.status_code == 200, response.text
    return response.json()
