# Test Cases for `Kanban_doska`

## Scope

Repository under test: `Prapor500/Kanban_doska`  
Local path: `/home/prapor05/Kanban_doska`

The source Word report includes both frontend and backend scenarios. This repository contains the backend only, so the execution set is split into:

- automated API tests that can be run inside this repository;
- documented manual or non-applicable cases for frontend-only behavior;
- additional regression checks for gaps found during analysis.

## Cases from the Word Report

| ID | Scenario | Repo coverage | Automation | Expected / observed status |
| --- | --- | --- | --- | --- |
| TC-01 | Register a new user with valid data | Backend auth API | Automated | PASS |
| TC-02 | Login with wrong password shows auth error | Backend auth API | Automated | PASS |
| TC-03 | Access to protected pages without auth redirects to login | Frontend routing only | Not applicable in this repo | N/A |
| TC-04 | Logout clears token/session and redirects | Frontend logout flow | Not applicable in this repo | N/A |
| UI-05 | Edit task title | Task API update | Automated | PASS |
| UI-06 | Cancel editing / close modal without saving | Frontend modal state | Manual only | N/A |
| UI-07 | Delete task with confirmation | Task API delete | Automated | PASS |
| UI-08 | Validate task field constraints | Task create/update validation | Automated regression | FAILING EXPECTATION |
| UI-09 | Create board and add columns | Projects + columns API | Automated | PASS |
| UI-10 | Forbid creating task with empty title | Task validation | Automated regression | FAILING EXPECTATION |
| UI-11 | Delete a column with tasks without server errors | Columns/task lifecycle | Automated regression | FAILING EXPECTATION |
| DND-12 | Move task within one column and preserve order after reload | Backend support for task ordering | Not supported by current schema | N/A |
| DND-13 | Move task to another column | Task update (`column_id`) | Automated | PASS |
| DND-14 | Rapid repeated moves | Task update stability | Partially covered by sequential updates | PASS |
| DND-15 | Work under slow connection | Network/UI behavior | Manual only | N/A |
| API-16 | Obtain token | `/auth/login` | Automated | PASS |
| API-17 | CRUD for projects | `/projects` | Automated | PASS |
| API-18 | CRUD for columns | `/columns` | Automated | PASS |
| API-19 | CRUD for tasks | `/tasks` | Automated | PASS |
| API-20 | Negative case with invalid identifier | 404 checks | Automated | PASS |
| API-21 | Partial task update | `PUT /tasks/{id}` | Automated | PASS |
| TC-22 | Create task, move it, reload, state is persisted | Task update + readback | Automated | PASS |
| TC-23 | Parallel edits in multiple tabs | Last-write-wins model | Automated approximation | PASS |
| TC-24 | Network loss during DnD and later resync | Network/UI behavior | Manual only | N/A |

## Additional Regression Cases

| ID | Scenario | Type | Expected / observed status |
| --- | --- | --- | --- |
| ADD-01 | Duplicate registration returns `400` | Automated | PASS |
| ADD-02 | Project creation should require auth | Automated regression | FAILING EXPECTATION |
| ADD-03 | `GET /tasks/?project_id=...` returns project-scoped tasks only | Automated regression | FAILING EXPECTATION |
| ADD-04 | User profile patch persists optional fields | Automated | PASS |
| ADD-05 | Delete non-empty column should not produce server-side integrity failure | Automated regression | FAILING EXPECTATION |
