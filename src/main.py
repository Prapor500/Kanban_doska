import uvicorn
import pyjokes
from fastapi import FastAPI
from src.settings import settings
from src.routers import router
from src.routers.v1.auth import auth

debug = settings.SERVER_TEST
app = FastAPI()
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/")
def joke():
    return pyjokes.get_joke()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.SERVER_ADDR,
        port=settings.SERVER_PORT,
        log_level="debug" if settings.SERVER_TEST else "info",
    )


# Подключите роутер
app.include_router(auth)
