from tests.helpers import create_column, create_project, create_task, register_user


def test_project_column_task_crud_flow(client):
    author_id = register_user(client, "author@example.com")
    assignee_id = register_user(client, "assignee@example.com")

    project = create_project(client, author_id, "Backend board")
    assert project["name"] == "Backend board"

    projects_response = client.get("/projects/")
    assert projects_response.status_code == 200
    assert projects_response.json() == [project]

    column = create_column(client, project["id"], "To Do", 1)
    assert column["project_id"] == project["id"]

    task = create_task(
        client,
        column_id=column["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Write API tests",
        description="Cover the CRUD flow",
    )
    assert task["title"] == "Write API tests"
    assert task["is_finished"] is False

    update_response = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Write more API tests", "is_finished": True},
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Write more API tests"
    assert updated_task["is_finished"] is True

    read_task_response = client.get(f"/tasks/{task['id']}")
    assert read_task_response.status_code == 200
    assert read_task_response.json()["title"] == "Write more API tests"

    delete_task_response = client.delete(f"/tasks/{task['id']}")
    assert delete_task_response.status_code == 200

    delete_column_response = client.delete(f"/columns/{column['id']}")
    assert delete_column_response.status_code == 200

    delete_project_response = client.delete(f"/projects/{project['id']}")
    assert delete_project_response.status_code == 200


def test_move_task_between_columns_persists_after_reload(client):
    author_id = register_user(client, "move-author@example.com")
    assignee_id = register_user(client, "move-assignee@example.com")
    project = create_project(client, author_id, "DnD parity")
    todo = create_column(client, project["id"], "To Do", 1)
    done = create_column(client, project["id"], "Done", 2)
    task = create_task(
        client,
        column_id=todo["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Move me",
    )

    move_response = client.put(
        f"/tasks/{task['id']}",
        json={"column_id": done["id"], "is_finished": True},
    )
    assert move_response.status_code == 200
    assert move_response.json()["column_id"] == done["id"]

    read_response = client.get(f"/tasks/{task['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["column_id"] == done["id"]
    assert read_response.json()["is_finished"] is True

    list_response = client.get("/tasks/")
    assert list_response.status_code == 200
    assert list_response.json()[0]["column_id"] == done["id"]


def test_missing_entities_return_404(client):
    missing_project = client.get("/projects/999")
    assert missing_project.status_code == 404
    assert missing_project.json()["detail"] == "Project not found"

    missing_column = client.delete("/columns/999")
    assert missing_column.status_code == 404
    assert missing_column.json()["detail"] == "Column not found"

    missing_task = client.put("/tasks/999", json={"title": "ghost"})
    assert missing_task.status_code == 404
    assert missing_task.json()["detail"] == "Task not found"


def test_last_write_wins_for_sequential_task_updates(client):
    author_id = register_user(client, "tab-author@example.com")
    assignee_id = register_user(client, "tab-assignee@example.com")
    project = create_project(client, author_id, "Concurrent edits")
    column = create_column(client, project["id"], "In Progress", 1)
    task = create_task(
        client,
        column_id=column["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Original title",
    )

    first_update = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Edited from tab 1"},
    )
    assert first_update.status_code == 200

    second_update = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Edited from tab 2"},
    )
    assert second_update.status_code == 200

    final_state = client.get(f"/tasks/{task['id']}")
    assert final_state.status_code == 200
    assert final_state.json()["title"] == "Edited from tab 2"


def test_profile_update_endpoint_updates_optional_fields(client):
    user_id = register_user(client, "profile@example.com")

    response = client.patch(
        f"/users/profile/{user_id}",
        json={
            "first_name": "Ivan",
            "last_name": "Petrov",
            "middle_name": "Sergeevich",
            "gender": "male",
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Профиль обновлен"

    get_user_response = client.get(f"/users/{user_id}")
    assert get_user_response.status_code == 200
    assert get_user_response.json()["first_name"] == "Ivan"
    assert get_user_response.json()["last_name"] == "Petrov"
