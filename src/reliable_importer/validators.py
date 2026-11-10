"""Row validation → Student domain object."""

from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Student


def parse_student(
    row: dict[str, str],
    *,
    line_number: int,
) -> Student:
    """Convert a CSV row into a Student; raise RecordValidationError."""

    # --- student_id ---
    raw_id = (row.get("student_id") or "").strip()
    try:
        student_id = int(raw_id)
    except (ValueError, TypeError) as error:
        raise RecordValidationError(
            "Invalid student ID",
            line_number=line_number,
            field="student_id",
        ) from error
    if student_id <= 0:
        raise RecordValidationError(
            "Student ID must be positive",
            line_number=line_number,
            field="student_id",
        )

    # --- name ---
    name = (row.get("name") or "").strip()
    if not name:
        raise RecordValidationError(
            "Student name is empty",
            line_number=line_number,
            field="name",
        )

    # --- group ---
    group = (row.get("group") or "").strip()
    if not group:
        raise RecordValidationError(
            "Group is empty",
            line_number=line_number,
            field="group",
        )

    # --- grade ---
    raw_grade = (row.get("grade") or "").strip()
    try:
        grade = float(raw_grade)
    except (ValueError, TypeError) as error:
        raise RecordValidationError(
            "Grade must be numeric",
            line_number=line_number,
            field="grade",
        ) from error
    if not 0.0 <= grade <= 100.0:
        raise RecordValidationError(
            "Grade must be between 0 and 100",
            line_number=line_number,
            field="grade",
        )

    # --- email ---
    email = (row.get("email") or "").strip()
    if "@" not in email:
        raise RecordValidationError(
            "Invalid email",
            line_number=line_number,
            field="email",
        )

    return Student(
        student_id=student_id,
        name=name,
        group=group,
        grade=grade,
        email=email,
    )
