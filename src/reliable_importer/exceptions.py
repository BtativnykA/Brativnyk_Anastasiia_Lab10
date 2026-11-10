"""Custom exception hierarchy."""


class ApplicationError(Exception):
    """Base exception for the whole application."""


class ConfigurationError(ApplicationError):
    """Configuration is invalid."""


class DataError(ApplicationError):
    """Base exception for data-related errors."""


class DataImportError(DataError):
    """Input data cannot be imported."""


class DataExportError(DataError):
    """Output data cannot be exported."""


class RecordValidationError(DataError):
    """A single record failed validation."""

    def __init__(
        self,
        message: str,
        *,
        line_number: int | None = None,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.line_number = line_number
        self.field = field

    def __str__(self) -> str:
        base = super().__str__()
        if self.line_number is not None:
            return f"line {self.line_number}: {base}"
        return base
