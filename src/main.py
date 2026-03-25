import uvicorn
from fastapi import FastAPI
from src.settings import settings
from src.routers import router
from src.routers.v1.auth import auth
from src.routers.v1.users import router_users
from src.routers.v1.columns import router_columns
from src.routers.v1.project_users import router_project_users
from src.routers.v1.projects import router_projects
from src.routers.v1.task_logs import router_task_logs
from src.routers.v1.tasks import router_tasks


debug = settings.SERVER_TEST
app = FastAPI()

app.include_router(router_users)
app.include_router(auth)
app.include_router(router_columns)
app.include_router(router_project_users)
app.include_router(router_projects)
app.include_router(router_task_logs)
app.include_router(router_tasks)
if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="debug" if settings.SERVER_TEST else "info",
    )
