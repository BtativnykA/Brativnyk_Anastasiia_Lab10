import pytest

from student_manager.models import Student
from student_manager.repositories import GroupRepository, StudentRepository
from student_manager.services import StudentService


@pytest.mark.integration
def test_add_and_get_student(db_session):
    group_repo = GroupRepository(db_session)
    student_repo = StudentRepository(db_session)
    group = group_repo.add("PI-21")

    student = Student(
        first_name="Anna", last_name="Koval", average_grade=91.5, group_id=group.id
    )
    saved = student_repo.add(student)

    assert saved.id is not None
    assert student_repo.get_by_id(saved.id).first_name == "Anna"


@pytest.mark.integration
def test_group_average(db_session):
    group = GroupRepository(db_session).add("PI-21")
    repo = StudentRepository(db_session)
    repo.add(
        Student(first_name="A", last_name="A", average_grade=90.0, group_id=group.id)
    )
    repo.add(
        Student(first_name="B", last_name="B", average_grade=80.0, group_id=group.id)
    )

    service = StudentService(db_session)
    assert service.get_group_average(group.id) == 85.0
