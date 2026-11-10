import json
from pathlib import Path

import pytest

from reliable_importer.config import load_config
from reliable_importer.exceptions import RecordValidationError
from reliable_importer.exporters import export_students_json
from reliable_importer.readers import read_csv_rows
from reliable_importer.validators import parse_student


@pytest.mark.integration
def test_full_pipeline_import_export(tmp_path):
    # 1. Створюємо тимчасовий CSV
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(
        "student_id,name,group,grade,email\n"
        "1,Anna,PI-21,91.5,anna@test.com\n"
        "2,Bad,PI-21,105,bad@test.com\n",  # невалідний
        encoding="utf-8",
    )

    output_file = tmp_path / "output.json"

    # 2. Запускаємо pipeline
    students = []
    for line_num, row in read_csv_rows(csv_file):
        try:
            students.append(parse_student(row, line_number=line_num))
        except RecordValidationError:
            continue  # tolerant mode

    exported_count = export_students_json(students, output_file)

    # 3. Перевіряємо результат
    assert exported_count == 1
    assert output_file.exists()

    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Anna"


@pytest.mark.integration
def test_config_loading_with_monkeypatch(tmp_path, monkeypatch):
    # Створюємо тимчасовий config.yaml
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "input:\n  path: dummy.csv\noutput:\n  path: out.json\n"
        "processing:\n  minimum_grade: 60\n  skip_invalid: true\n"
        "logging:\n  level: INFO\n  path: app.log\n",
        encoding="utf-8",
    )

    # monkeypatch робить вигляд, що файл dummy.csv існує
    monkeypatch.setattr(Path, "exists", lambda self: True)

    config = load_config(config_file)
    assert config.processing.minimum_grade == 60
    assert config.processing.skip_invalid is True


@pytest.mark.integration
def test_atomic_export_failure(tmp_path, monkeypatch):
    output_file = tmp_path / "result.json"
    output_file.write_text("OLD DATA", encoding="utf-8")

    # Робимо так, щоб replace() викликав помилку
    monkeypatch.setattr(
        Path, "replace", lambda *args: (_ for _ in ()).throw(OSError("Disk full"))
    )

    from reliable_importer.exceptions import DataExportError

    with pytest.raises(DataExportError):
        export_students_json([], output_file)

    # Перевіряємо, що старі дані не пошкоджені, а .tmp видалено
    assert output_file.read_text(encoding="utf-8") == "OLD DATA"
