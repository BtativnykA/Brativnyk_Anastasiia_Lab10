import pytest

from reliable_importer.exceptions import RecordValidationError
from reliable_importer.validators import parse_student


def test_valid_row_parsing():
    row = {
        "student_id": "1",
        "name": "Anna",
        "group": "PI-21",
        "grade": "91.5",
        "email": "a@b.com",
    }
    student = parse_student(row, line_number=2)
    assert student.student_id == 1


def test_empty_name_raises_validation_error():
    row = {
        "student_id": "1",
        "name": "",
        "group": "PI-21",
        "grade": "91.5",
        "email": "a@b.com",
    }
    with pytest.raises(RecordValidationError) as exc_info:
        parse_student(row, line_number=2)

    assert exc_info.value.field == "name"
    assert exc_info.value.line_number == 2


def test_invalid_id_exception_chaining():
    row = {
        "student_id": "abc",
        "name": "Anna",
        "group": "PI-21",
        "grade": "91.5",
        "email": "a@b.com",
    }
    with pytest.raises(RecordValidationError) as exc_info:
        parse_student(row, line_number=5)

    # Перевірка exception chaining (ValueError -> RecordValidationError)
    assert isinstance(exc_info.value.__cause__, ValueError)
    assert exc_info.value.field == "student_id"
