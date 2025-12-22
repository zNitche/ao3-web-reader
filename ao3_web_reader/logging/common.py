from typing import Any
import os
from logging import Logger, Formatter, StreamHandler, LoggerAdapter
from logging.handlers import TimedRotatingFileHandler


def setup(logger: Logger, logs_path: str | None, is_debug: bool, backup_log_files_count: int | None):
    if is_debug:
        logger.setLevel("DEBUG")
    else:
        logger.setLevel("INFO")

    setup_serial(logger=logger)

    if logs_path is not None and backup_log_files_count is not None:
        setup_logs_file(path=logs_path, logger=logger,
                        backup_log_files_count=backup_log_files_count)


def set_logs_path(filename: str | None, path: str | None) -> str | None:
    if filename is None or path is None:
        return None

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    return os.path.join(path, filename)


def setup_serial(logger: Logger | LoggerAdapter[Any]):
    formatter = get_formatter(with_day=False)

    console_logger = StreamHandler()
    console_logger.setFormatter(formatter)

    logger.addHandler(console_logger)  # type: ignore


def setup_logs_file(logger: Logger | LoggerAdapter[Any], path: str, backup_log_files_count: int):
    formatter = get_formatter()

    file_handler = TimedRotatingFileHandler(filename=path,
                                            when="midnight",
                                            encoding="utf-8",
                                            backupCount=backup_log_files_count)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)  # type: ignore


def get_formatter(with_day: bool = True) -> Formatter:
    format = "%Y-%m-%d %H:%M:%S" if with_day else "%H:%M:%S"

    formatter = Formatter(
        "{asctime} - {name} - {levelname} - {message}",
        style="{",
        datefmt=format,
    )

    return formatter
