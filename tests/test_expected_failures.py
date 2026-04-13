import pytest

from tests.helpers import create_column, create_project, create_task, register_user


@pytest.mark.xfail(
    reason="Маршруты проектов не защищены авторизацией и принимают запросы без токена.",
    strict=False,
)
def test_create_project_requires_authentication(client):
    user_id = register_user(client, "public-route@example.com")

    response = client.post(
        "/projects/",
        json={"created_by": user_id, "name": "Should require auth"},
    )

    assert response.status_code in {401, 403}


@pytest.mark.xfail(
    reason="Бэкенд сейчас принимает пустой title, хотя в отчете сценарий описан как запрещенный.",
    strict=False,
)
def test_create_task_with_empty_title_is_rejected(client):
    author_id = register_user(client, "empty-title-author@example.com")
    assignee_id = register_user(client, "empty-title-assignee@example.com")
    project = create_project(client, author_id, "Validation gaps")
    column = create_column(client, project["id"], "To Do", 1)

    response = client.post(
        "/tasks/",
        json={
            "column_id": column["id"],
            "created_by": author_id,
            "assigned_to": assignee_id,
            "title": "",
            "description": "Should not pass",
            "is_finished": False,
        },
    )

    assert response.status_code in {400, 422}


@pytest.mark.xfail(
    reason="GET /tasks/ игнорирует project_id, хотя в отчете этот фильтр участвует в DnD-синхронизации.",
    strict=False,
)
def test_tasks_endpoint_filters_by_project_id(client):
    author_id = register_user(client, "filter-author@example.com")
    assignee_id = register_user(client, "filter-assignee@example.com")

    project_a = create_project(client, author_id, "Project A")
    column_a = create_column(client, project_a["id"], "A", 1)
    task_a = create_task(
        client,
        column_id=column_a["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Task A",
    )

    project_b = create_project(client, author_id, "Project B")
    column_b = create_column(client, project_b["id"], "B", 1)
    create_task(
        client,
        column_id=column_b["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Task B",
    )

    response = client.get(f"/tasks/?project_id={project_a['id']}")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [task_a["id"]]


@pytest.mark.xfail(
    reason="Удаление колонки с задачами сейчас не обрабатывается как безопасный сценарий без серверной ошибки.",
    strict=False,
)
def test_delete_column_with_tasks_does_not_error(client):
    author_id = register_user(client, "delete-column-author@example.com")
    assignee_id = register_user(client, "delete-column-assignee@example.com")
    project = create_project(client, author_id, "Column delete gap")
    column = create_column(client, project["id"], "To Delete", 1)
    create_task(
        client,
        column_id=column["id"],
        created_by=author_id,
        assigned_to=assignee_id,
        title="Task in column",
    )

    response = client.delete(f"/columns/{column['id']}")

    assert response.status_code in {200, 204}
