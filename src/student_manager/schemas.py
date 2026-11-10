"""Pydantic schemas for API validation and serialization."""

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    group_id: int = Field(gt=0)
    average_grade: float = Field(ge=0, le=100)


class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = Field(default=None, gt=0)
    average_grade: float | None = Field(default=None, ge=0, le=100)


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    group_id: int
    average_grade: float

    # Дозволяє Pydantic читати дані з ORM-моделей SQLAlchemy
    model_config = {"from_attributes": True}


class GroupStatistics(BaseModel):
    group_id: int
    students_count: int
    average_grade: float
