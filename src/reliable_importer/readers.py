"""Streaming CSV reader."""

import csv
from collections.abc import Iterator
from pathlib import Path

from reliable_importer.exceptions import DataImportError


def read_csv_rows(
    path: Path,
) -> Iterator[tuple[int, dict[str, str]]]:
    """Yield (line_number, row) tuples lazily.

    Line numbers start at 2 (after the header).
    """
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            yield from enumerate(reader, start=2)
    except OSError as error:
        raise DataImportError(f"Cannot read input file: {path}") from error
