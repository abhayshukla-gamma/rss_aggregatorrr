# ................................................................................. app/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db, Base



# ...................................................................................TEST DATABASE (Fresh Every Run)


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost:5432/rss_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Drop & recreate tables each test session
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ............................................................................ REMOVE STARTUP EVENTS


app.router.on_startup.clear()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
