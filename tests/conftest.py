import os
import sys
import types

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DB_USERNAME", "postgres")
os.environ.setdefault("DB_PASSWORD", "postgres")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_ADDR", "127.0.0.1")
os.environ.setdefault("DB_PORT", "5432")

import src.models.column  # noqa: F401
import src.models.project  # noqa: F401
import src.models.project_user  # noqa: F401
import src.models.task  # noqa: F401
import src.models.task_log  # noqa: F401
import src.models.user  # noqa: F401
from src.core.services.db import get_db

jwt_backend_stub = types.ModuleType("src.infrastructure.jwt_backend")


def make_access_token(payload, exp=None):
    subject = payload.get("sub", "test-user")
    return f"test-token-for-{subject}"


def verify_token(token, *, check_exp=True):
    return {"sub": token.removeprefix("test-token-for-")}


jwt_backend_stub.make_access_token = make_access_token
jwt_backend_stub.verify_token = verify_token
sys.modules["src.infrastructure.jwt_backend"] = jwt_backend_stub

from src.main import app
from src.models.base import Base


@pytest.fixture()
def session_factory(tmp_path):
    db_path = tmp_path / "test.sqlite3"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        yield factory
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
