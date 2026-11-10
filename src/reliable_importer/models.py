from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Student:
    student_id: int
    name: str
    group: str
    grade: float
    email: str

    def __post_init__(self) -> None:
        # Додаємо валідацію, якої не було в Лабораторній №5
        if not 0.0 <= self.grade <= 100.0:
            raise ValueError(f"Grade must be between 0 and 100, got {self.grade}")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


# (Решта файлу - ProcessingConfig, LoggingConfig, AppConfig - залишається без змін)
@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    minimum_grade: float
    skip_invalid: bool


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path


@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig
