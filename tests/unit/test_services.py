from unittest.mock import Mock

import pytest

from reliable_importer.registry import InMemoryRepository, StudentRegistryService


def test_register_student_success(sample_student, mock_notifier):
    repo = InMemoryRepository()
    service = StudentRegistryService(repo, mock_notifier)

    service.register(sample_student)

    # Interaction assertion (перевірка, що метод викликано правильно)
    mock_notifier.send.assert_called_once_with("anna@test.com", "Welcome Anna Koval!")
    assert repo.get(1) == sample_student


def test_register_duplicate_raises_error(sample_student, mock_notifier):
    repo = InMemoryRepository()
    service = StudentRegistryService(repo, mock_notifier)
    service.register(sample_student)

    with pytest.raises(ValueError, match="already exists"):
        service.register(sample_student)


def test_notifier_failure_propagates(sample_student):
    repo = InMemoryRepository()
    mock_notifier = Mock()
    # side_effect — імітуємо помилку зовнішнього сервісу
    mock_notifier.send.side_effect = ConnectionError("SMTP server down")

    service = StudentRegistryService(repo, mock_notifier)

    with pytest.raises(ConnectionError):
        service.register(sample_student)


def test_get_best_student(sample_students, mock_notifier):
    repo = InMemoryRepository()
    for s in sample_students:
        repo.add(s)

    service = StudentRegistryService(repo, mock_notifier)
    best = service.get_best_student()

    assert best is not None
    assert best.name == "Iryna Bondar"
    assert best.grade == 95.2
