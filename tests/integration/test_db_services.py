import pytest

from student_manager.models import Student
from student_manager.repositories import GroupRepository, StudentRepository
from student_manager.services import transfer_students


@pytest.mark.integration
def test_transfer_rollback(db_session):
    group_repo = GroupRepository(db_session)
    g1 = group_repo.add("PI-21")
    g2 = group_repo.add("PI-22")

    repo = StudentRepository(db_session)
    student = repo.add(
        Student(
            first_name="Anna", last_name="Koval", average_grade=91.5, group_id=g1.id
        )
    )

    # Намагаємось перевести існуючого та НЕіснуючого студента
    with pytest.raises(ValueError):
        transfer_students(db_session, [student.id, 999999], g2.id)

    # Перевіряємо, що зміни відкотилися (rollback)
    db_session.refresh(student)
    assert student.group_id == g1.id
