from unittest.mock import AsyncMock

import pytest

from reliable_importer.async_services import AsyncStudentReportService


@pytest.mark.asyncio
async def test_generate_report_success():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.fetch_student.return_value = {"name": "Anna", "grade": 95}
    service = AsyncStudentReportService(mock_repo)

    # Act
    result = await service.generate_report(1)

    # Assert
    assert result == "Report for Anna: 95"
    mock_repo.fetch_student.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_generate_report_not_found():
    mock_repo = AsyncMock()
    mock_repo.fetch_student.return_value = None
    service = AsyncStudentReportService(mock_repo)

    result = await service.generate_report(99)
    assert result == "Not found"
