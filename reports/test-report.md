# Test Execution Report for `Kanban_doska`

## Basis

- Repository: `Prapor500/Kanban_doska`
- Local path: `/home/prapor05/Kanban_doska`
- Source document: `/home/prapor05/Downloads/Telegram Desktop/Отчёт_Проектный_практикум_Канбан_доска.docx`
- Test focus: backend API, backend-supported integrations, and gap analysis against the report

## Environment

- Python: `3.12.3`
- Test runner: `pytest 9.0.2`
- Test isolation: `FastAPI TestClient` + temporary SQLite database per test

## Implemented Test Assets

- `tests/test_auth_api.py`
- `tests/test_workflows_api.py`
- `tests/test_expected_failures.py`
- `tests/conftest.py`
- `reports/test-cases.md`

## Notes Before Execution

- This repository contains the backend only. Frontend-only scenarios from the source report cannot be executed here as automated tests.
- The current backend schema does not contain task ordering fields, so same-column DnD reorder persistence cannot be validated in this repository.
- Some report assumptions do not match the current backend implementation. These are captured as regression tests marked with `xfail`.
- `src.infrastructure.jwt_backend` could not be imported as-is in the test environment because `jamlib` raises `JamStarlettePluginConfigError` (`cookie_name or header_name must be provided`). The test bootstrap replaces this module with a minimal stub so the FastAPI app can be loaded and the repository’s own route logic can still be exercised.

## Results

- Main run:
  - Command: `/home/prapor05/Kanban_doska/.venv/bin/pytest -q /home/prapor05/Kanban_doska`
  - Result: `7 passed, 4 xfailed, 9 warnings`
- Focused mismatch run:
  - Command: `/home/prapor05/Kanban_doska/.venv/bin/pytest -q --runxfail /home/prapor05/Kanban_doska/tests/test_expected_failures.py`
  - Result: `4 failed` as expected, used only to capture exact current behavior

## Passed Coverage

- User registration works and duplicate email is rejected with `400`.
- Login with valid credentials returns `access_token` and `token_type`.
- Login with invalid password returns `401`.
- CRUD flow for project, column, and task works in the basic happy path.
- Moving a task to another column via `PUT /tasks/{id}` persists after readback.
- Missing entities return `404`.
- Sequential task edits behave as `last write wins`.
- `PATCH /users/profile/{user_id}` persists optional profile fields.

## Confirmed Gaps

- Unauthenticated project creation succeeds with `200 OK` instead of `401/403`.
- Creating a task with an empty `title` succeeds with `200 OK`.
- `GET /tasks/?project_id=<id>` ignores the filter and returned `[1, 2]` instead of `[1]` in the regression check.
- Deleting a column that still has tasks raises `sqlalchemy.exc.IntegrityError` caused by `NOT NULL constraint failed: task.column_id`.

## Warnings Observed

- SQLAlchemy deprecation warning for `declarative_base()` import style in `src/models/base.py`.
- Pydantic V2 deprecation warning for class-based config in `src/schemas/users.py`.
- Deprecation warning for `datetime.datetime.utcnow()` used in SQLAlchemy defaults.

## Preliminary Findings

- Authentication exists only on `/auth/*`; project, column, and task routes are currently accessible without token-based protection.
- The backend accepts an empty task title, which conflicts with the report’s “forbid empty title” scenario.
- `GET /tasks/` does not filter by `project_id`, even though the report text references that query shape during DnD resynchronization.
- The current delete flow for non-empty columns is unsafe and breaks on database integrity checks instead of returning an application-level response.
- JWT integration has a configuration defect that prevents importing the backend without a workaround in tests.
