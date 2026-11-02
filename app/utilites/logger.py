import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR/"logs"

LOG_DIR.mkdir(parents=True,exist_ok=True)

logger=logging.getLogger("project_management")
logger.setLevel(logging.INFO)
logger.propagate = False

format=logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

if not logger.handlers:

    file_handler = RotatingFileHandler(
        LOG_DIR/"app.log",
        maxBytes= 5*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setFormatter(format)

    logger.addHandler(file_handler)

    