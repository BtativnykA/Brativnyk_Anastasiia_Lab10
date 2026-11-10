"""Application entry point."""

import logging
from pathlib import Path

from reliable_importer.config import load_config
from reliable_importer.context_managers import logged_operation
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_students_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import (
    ImportStatistics,
    filter_by_grade,
    import_students,
)

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
    except ApplicationError as error:
        # before logging is configured — print to stderr
        print(f"[FATAL] {error}")
        raise SystemExit(1) from error

    configure_logging(config.logging.level, config.logging.path)

    try:
        with logged_operation("Student import/export"):
            statistics = ImportStatistics()

            # stream + validate + filter
            valid_stream = import_students(
                config.input_path,
                skip_invalid=config.processing.skip_invalid,
                statistics=statistics,
            )
            filtered = filter_by_grade(
                valid_stream,
                config.processing.minimum_grade,
            )

            exported = export_students_json(
                filtered,
                config.output_path,
            )

        logger.info(
            "Total=%d, valid=%d, invalid=%d, exported=%d",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported,
        )

    except ApplicationError:
        logger.exception("Application failed")
        raise SystemExit(2)
    except Exception:
        logger.exception("Unexpected error")
        raise SystemExit(3)


if __name__ == "__main__":
    main()
