import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging():

    # Project root
    BASE_DIR = Path(__file__).resolve().parent

    # logs folder
    LOG_DIR = BASE_DIR / "logs"

    # Create folder automatically if it doesn't exist
    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Log file
    LOG_FILE = LOG_DIR / "orchestrator.log"

    # Root logger
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return

    # Format
    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    # -------------------------------------------------------
    # Console logging
    # -------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    # -------------------------------------------------------
    # File logging
    # -------------------------------------------------------

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        formatter
    )

    # Add handlers
    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )

    logger.info(
        f"Logging initialized. "
        f"Log file: {LOG_FILE}"
    )