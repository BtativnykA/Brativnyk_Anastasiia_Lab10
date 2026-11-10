"""Registry service that uses external dependencies (Notifier, Repo)."""

from typing import Protocol

from reliable_importer.models import Student


class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None: ...


class InMemoryRepository:
    def __init__(self) -> None:
        self._items: dict[int, Student] = {}

    def add(self, student: Student) -> None:
        self._items[student.student_id] = student

    def get(self, student_id: int) -> Student | None:
        return self._items.get(student_id)

    def all(self) -> list[Student]:
        return list(self._items.values())


class StudentRegistryService:
    def __init__(self, repository: InMemoryRepository, notifier: Notifier) -> None:
        self._repo = repository
        self._notifier = notifier

    def register(self, student: Student) -> None:
        if self._repo.get(student.student_id) is not None:
            raise ValueError(f"Student {student.student_id} already exists")
        self._repo.add(student)
        self._notifier.send(student.email, f"Welcome {student.name}!")

    def get_best_student(self) -> Student | None:
        students = self._repo.all()
        if not students:
            return None
        return max(students, key=lambda s: s.grade)
