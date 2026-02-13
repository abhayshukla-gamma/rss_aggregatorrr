# app/tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db, Base


# -------------------------------------------------------------------
# DATABASE CONFIG (Works Locally + In GitHub Actions)
# -------------------------------------------------------------------

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:12345@localhost:5432/rss_db"  # local fallback
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------------------------------------------------
# CREATE & DROP TABLES SAFELY
# -------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Wait briefly in case DB container is still starting (CI safety)
    import time
    time.sleep(2)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# -------------------------------------------------------------------
# OVERRIDE DEPENDENCY
# -------------------------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# -------------------------------------------------------------------
# DISABLE STARTUP EVENTS (Optional but Good for Tests)
# -------------------------------------------------------------------

app.router.on_startup.clear()


# -------------------------------------------------------------------
# TEST CLIENT
# -------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
