"""Configuration loader with validation (fail-fast)."""

from pathlib import Path

import yaml

from reliable_importer.exceptions import ConfigurationError
from reliable_importer.models import (
    AppConfig,
    LoggingConfig,
    ProcessingConfig,
)


def load_config(path: Path) -> AppConfig:
    """Load YAML config; raise ConfigurationError on any problem."""
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Configuration file not found: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Invalid YAML configuration") from error

    if not isinstance(raw, dict):
        raise ConfigurationError("Config root must be a mapping")

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                minimum_grade=float(raw["processing"]["minimum_grade"]),
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Configuration structure is invalid") from error

    _validate_config(config)
    return config


def _validate_config(config: AppConfig) -> None:
    """Fail-fast checks for configuration."""
    if not 0.0 <= config.processing.minimum_grade <= 100.0:
        raise ConfigurationError("minimum_grade must be between 0 and 100")
    if not config.input_path.exists():
        raise ConfigurationError(f"Input file not found: {config.input_path}")
    if config.input_path.suffix.lower() != ".csv":
        raise ConfigurationError("Only .csv input is supported for Variant 1")
