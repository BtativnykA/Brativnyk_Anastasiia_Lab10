"""Business logic and transactional operations."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from student_manager.models import Student


class StudentService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_group_average(self, group_id: int) -> float:
        statement = select(func.avg(Student.average_grade)).where(
            Student.group_id == group_id
        )
        result = self.session.scalar(statement)
        return float(result) if result is not None else 0.0

    def get_best_student(self) -> Student | None:
        statement = select(Student).order_by(Student.average_grade.desc()).limit(1)
        return self.session.scalar(statement)


def transfer_students(
    session: Session, student_ids: list[int], new_group_id: int
) -> None:
    """Транзакційна операція масового переведення (rollback при помилці)."""
    try:
        for student_id in student_ids:
            student = session.get(Student, student_id)
            if student is None:
                raise ValueError(f"Student {student_id} not found")
            student.group_id = new_group_id
        session.commit()
    except Exception:
        session.rollback()
        raise
