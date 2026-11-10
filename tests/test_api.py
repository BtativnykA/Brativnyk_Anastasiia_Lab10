from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from student_manager.api import app
from student_manager.dependencies import get_session
from student_manager.models import Base

# Використовуємо StaticPool, щоб база в пам'яті була спільною для всіх підключень
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

Base.metadata.create_all(bind=engine)


def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


def test_create_and_get_student():
    response = client.post(
        "/students",
        json={
            "first_name": "Anna",
            "last_name": "Koval",
            "group_id": 1,
            "average_grade": 150,  # Невалідне значення
        },
    )
    assert response.status_code == 422


def test_get_missing_student():
    response = client.get("/students/9999")
    assert response.status_code == 404
