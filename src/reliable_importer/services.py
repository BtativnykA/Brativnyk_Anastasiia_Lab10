"""Import service: streaming validation + filtering + statistics."""

import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Student
from reliable_importer.readers import read_csv_rows
from reliable_importer.validators import parse_student

logger = logging.getLogger(__name__)


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0


def import_students(
    path: Path,
    skip_invalid: bool,
    statistics: ImportStatistics,
) -> Iterator[Student]:
    """Stream valid students; record statistics; honor strict/tolerant mode."""
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            student = parse_student(row, line_number=line_number)
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning(
                "Invalid record at line %s: %s",
                error.line_number,
                error,
            )
            if skip_invalid:
                continue
            raise
        statistics.valid += 1
        yield student


def filter_by_grade(
    students: Iterable[Student],
    minimum_grade: float,
) -> Iterator[Student]:
    """Yield students with grade >= minimum."""
    for student in students:
        if student.grade >= minimum_grade:
            yield student
