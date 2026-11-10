"""Async services to demonstrate AsyncMock testing."""

from typing import Any


class AsyncStudentRepository:
    async def fetch_student(self, student_id: int) -> dict[str, Any] | None:
        raise NotImplementedError


class AsyncStudentReportService:
    def __init__(self, repository: AsyncStudentRepository) -> None:
        self._repo = repository

    async def generate_report(self, student_id: int) -> str:
        data = await self._repo.fetch_student(student_id)
        if data is None:
            return "Not found"
        return f"Report for {data['name']}: {data['grade']}"
