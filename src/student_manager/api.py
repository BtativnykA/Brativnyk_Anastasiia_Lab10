"""FastAPI application for Student Manager."""

import asyncio

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from student_manager.dependencies import get_session
from student_manager.external_api import fetch_many_stats
from student_manager.models import Student
from student_manager.repositories import StudentRepository
from student_manager.schemas import (
    GroupStatistics,
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from student_manager.services import StudentService

app = FastAPI(title="Student Manager API", version="1.0.0")

from fastapi import FastAPI

from student_manager.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


# --- CRUD for Students ---


@app.get("/students", response_model=list[StudentResponse])
async def get_students(session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    return repo.get_all()


@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    student = repo.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post(
    "/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED
)
async def create_student(data: StudentCreate, session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    student = Student(
        first_name=data.first_name,
        last_name=data.last_name,
        group_id=data.group_id,
        average_grade=data.average_grade,
    )
    return repo.add(student)


@app.patch("/students/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int, data: StudentUpdate, session: Session = Depends(get_session)
):
    repo = StudentRepository(session)
    student = repo.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(student, field, value)

    session.commit()
    session.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    if not repo.delete(student_id):
        raise HTTPException(status_code=404, detail="Student not found")


# --- Groups and Statistics ---


@app.get("/groups/{group_id}/students", response_model=list[StudentResponse])
async def get_group_students(group_id: int, session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    return repo.find_by_group(group_id)


@app.get("/groups/{group_id}/statistics", response_model=GroupStatistics)
async def get_group_statistics(group_id: int, session: Session = Depends(get_session)):
    repo = StudentRepository(session)
    service = StudentService(session)

    students = repo.find_by_group(group_id)
    if not students:
        raise HTTPException(
            status_code=404, detail="Group has no students or not found"
        )

    avg = service.get_group_average(group_id)
    return GroupStatistics(
        group_id=group_id, students_count=len(students), average_grade=avg
    )


# --- Async Batch Endpoint (Task + gather + Semaphore + timeout) ---


@app.post("/groups/statistics/batch")
async def batch_group_statistics(group_ids: list[int]):
    try:
        # Загальний таймаут на всю операцію
        results = await asyncio.wait_for(fetch_many_stats(group_ids), timeout=10.0)
        return results
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Batch operation timed out")
