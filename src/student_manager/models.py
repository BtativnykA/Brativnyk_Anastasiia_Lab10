"""SQLAlchemy ORM models."""

from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Зв'язок One-to-Many (одна група має багато студентів)
    students: Mapped[list[Student]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    average_grade: Mapped[float] = mapped_column(Float, nullable=False)

    # Зовнішній ключ (Foreign Key)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)

    # Поле email з'явиться після міграції (поки що nullable)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    group: Mapped[Group] = relationship(back_populates="students")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
