"""Repositories for interacting with the database."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from student_manager.models import Group, Student


class GroupRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Group:
        group = Group(name=name)
        self.session.add(group)
        self.session.commit()
        self.session.refresh(group)
        return group

    def get_by_name(self, name: str) -> Group | None:
        statement = select(Group).where(Group.name == name)
        return self.session.scalar(statement)


class StudentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, student: Student) -> Student:
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    def get_by_id(self, student_id: int) -> Student | None:
        return self.session.get(Student, student_id)

    def get_all(self) -> list[Student]:
        return list(self.session.scalars(select(Student)))

    def find_by_last_name(self, last_name: str) -> list[Student]:
        statement = select(Student).where(Student.last_name == last_name)
        return list(self.session.scalars(statement))

    def find_by_group(self, group_id: int) -> list[Student]:
        statement = select(Student).where(Student.group_id == group_id)
        return list(self.session.scalars(statement))

    def update_grade(self, student_id: int, grade: float) -> Student | None:
        student = self.get_by_id(student_id)
        if student is None:
            return None
        student.average_grade = grade
        self.session.commit()
        self.session.refresh(student)
        return student

    def delete(self, student_id: int) -> bool:
        student = self.get_by_id(student_id)
        if student is None:
            return False
        self.session.delete(student)
        self.session.commit()
        return True
