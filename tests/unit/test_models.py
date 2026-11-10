import pytest

from reliable_importer.models import Student


def test_student_creation_valid(sample_student):
    assert sample_student.name == "Anna Koval"
    assert sample_student.student_id == 1


@pytest.mark.parametrize(
    "grade", [0, 0.01, 50.0, 99.99, 100], ids=["min", "min+", "mid", "max-", "max"]
)
def test_valid_grade_boundaries(grade):
    # Arrange & Act
    student = Student(1, "Test", "PI-21", grade, "test@test.com")
    # Assert
    assert student.grade == pytest.approx(grade)


@pytest.mark.parametrize("invalid_grade", [-0.01, -10, 100.01, 105])
def test_invalid_grade_raises_value_error(invalid_grade):
    with pytest.raises(ValueError, match="Grade must be between 0 and 100"):
        Student(1, "Test", "PI-21", invalid_grade, "test@test.com")


def test_student_to_dict(sample_student):
    data = sample_student.to_dict()
    assert data["student_id"] == 1
    assert data["name"] == "Anna Koval"
    assert "email" in data
