import uvicorn
from fastapi import FastAPI
from src.settings import settings
from src.routers import router
from src.routers.v1.auth import auth
from src.models import User, Project, Column, ProjectUser, TaskLog, Task


debug = settings.SERVER_TEST
app = FastAPI()
app.include_router(router)
app.include_router(auth)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="debug" if settings.SERVER_TEST else "info",
    )
