from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Імпорти для Лабораторної №6 (фікстури для reliable_importer)
from reliable_importer.models import Student as ImporterStudent

# Імпорт для Лабораторної №7 (база даних)
from student_manager.models import Base

# ==========================================
# ФІКСТУРИ З ЛАБОРАТОРНОЇ №6 (для старих тестів)
# ==========================================


@pytest.fixture
def sample_student() -> ImporterStudent:
    return ImporterStudent(
        student_id=1,
        name="Anna Koval",
        group="PI-21",
        grade=91.5,
        email="anna@test.com",
    )


@pytest.fixture
def sample_students() -> list[ImporterStudent]:
    return [
        ImporterStudent(1, "Anna Koval", "PI-21", 91.5, "anna@test.com"),
        ImporterStudent(2, "Oleh Melnyk", "PI-21", 84.0, "oleh@test.com"),
        ImporterStudent(3, "Iryna Bondar", "PI-22", 95.2, "iryna@test.com"),
    ]


@pytest.fixture
def mock_notifier():
    return Mock()


# ==========================================
# ФІКСТУРИ З ЛАБОРАТОРНОЇ №7 (для тестів БД)
# ==========================================


@pytest.fixture
def db_session() -> Session:
    """Створює ізольовану БД в пам'яті для кожного тесту."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)

    with TestSession() as session:
        yield session

    Base.metadata.drop_all(engine)
