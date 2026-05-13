import os
import sys

os.environ.pop("SECRET_KEY", None)
os.environ["SECRET_KEY"] = "my_fixed_test_key_123"
os.environ["PYTHON_DOTENV_DOTENV"] = "0"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import User, Vacancy, Application
from app.auth import get_password_hash, create_access_token

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_user(db, email, role, password="secret"):
    user = User(email=email, hashed_password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def auth_header(user_id):
    token = create_access_token({"sub": user_id})
    return {"Authorization": f"Bearer {token}"}