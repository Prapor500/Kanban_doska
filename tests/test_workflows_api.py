from tests.helpers import create_column, create_project, create_task, register_user, login_user


def test_project_column_task_crud_flow(client):
    register_user(client, "author@example.com")
    headers = login_user(client, "author@example.com")
    
    assignee_id = register_user(client, "assignee@example.com")

    project = create_project(client, headers, "Backend board")
    assert project["name"] == "Backend board"

    projects_response = client.get("/projects/", headers=headers)
    assert projects_response.status_code == 200
    assert any(p["id"] == project["id"] for p in projects_response.json())

    column = create_column(client, headers, project["id"], "To Do", 1)
    assert column["project_id"] == project["id"]

    task = create_task(
        client,
        headers,
        column_id=column["id"],
        assigned_to=assignee_id,
        title="Write API tests",
        description="Cover the CRUD flow",
    )
    assert task["title"] == "Write API tests"
    assert task["is_finished"] is False

    update_response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Write more API tests", "is_finished": True},
        headers=headers
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Write more API tests"
    assert updated_task["is_finished"] is True

    read_task_response = client.get(f"/tasks/{task['id']}", headers=headers)
    assert read_task_response.status_code == 200
    assert read_task_response.json()["title"] == "Write more API tests"

    delete_task_response = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert delete_task_response.status_code == 200

    delete_column_response = client.delete(f"/columns/{column['id']}", headers=headers)
    assert delete_column_response.status_code == 200

    delete_project_response = client.delete(f"/projects/{project['id']}", headers=headers)
    assert delete_project_response.status_code == 200


def test_move_task_between_columns_persists_after_reload(client):
    register_user(client, "move-author@example.com")
    headers = login_user(client, "move-author@example.com")
    
    assignee_id = register_user(client, "move-assignee@example.com")
    
    project = create_project(client, headers, "DnD parity")
    todo = create_column(client, headers, project["id"], "To Do", 1)
    done = create_column(client, headers, project["id"], "Done", 2)
    task = create_task(
        client,
        headers,
        column_id=todo["id"],
        assigned_to=assignee_id,
        title="Move me",
    )

    move_response = client.put(
        f"/tasks/{task['id']}",
        json={"column_id": done["id"], "is_finished": True},
        headers=headers
    )
    assert move_response.status_code == 200
    assert move_response.json()["column_id"] == done["id"]

    read_response = client.get(f"/tasks/{task['id']}", headers=headers)
    assert read_response.status_code == 200
    assert read_response.json()["column_id"] == done["id"]
    assert read_response.json()["is_finished"] is True

    list_response = client.get("/tasks/", headers=headers)
    assert list_response.status_code == 200
    assert any(t["id"] == task["id"] and t["column_id"] == done["id"] for t in list_response.json())


def test_missing_entities_return_404(client):
    register_user(client, "ghost@example.com")
    headers = login_user(client, "ghost@example.com")

    missing_project = client.get("/projects/999", headers=headers)
    assert missing_project.status_code == 404

    missing_column = client.delete("/columns/999", headers=headers)
    assert missing_column.status_code == 404

    missing_task = client.put("/tasks/999", json={"title": "ghost"}, headers=headers)
    assert missing_task.status_code == 404


def test_last_write_wins_for_sequential_task_updates(client):
    register_user(client, "tab-author@example.com")
    headers = login_user(client, "tab-author@example.com")
    
    assignee_id = register_user(client, "tab-assignee@example.com")
    
    project = create_project(client, headers, "Concurrent edits")
    column = create_column(client, headers, project["id"], "In Progress", 1)
    task = create_task(
        client,
        headers,
        column_id=column["id"],
        assigned_to=assignee_id,
        title="Original title",
    )

    first_update = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Edited from tab 1"},
        headers=headers
    )
    assert first_update.status_code == 200

    second_update = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Edited from tab 2"},
        headers=headers
    )
    assert second_update.status_code == 200

    final_state = client.get(f"/tasks/{task['id']}", headers=headers)
    assert final_state.status_code == 200
    assert final_state.json()["title"] == "Edited from tab 2"


def test_profile_update_endpoint_updates_optional_fields(client):
    user_id = register_user(client, "profile@example.com")
    headers = login_user(client, "profile@example.com")

    response = client.patch(
        f"/users/profile/{user_id}",
        json={
            "first_name": "Ivan",
            "last_name": "Petrov",
            "middle_name": "Sergeevich",
            "gender": "male",
        },
        headers=headers
    )
    assert response.status_code == 200
    # response is UserOut, not a message dict
    assert response.json()["first_name"] == "Ivan"

    get_user_response = client.get(f"/users/{user_id}", headers=headers)
    assert get_user_response.status_code == 200
    assert get_user_response.json()["first_name"] == "Ivan"
    assert get_user_response.json()["last_name"] == "Petrov"
