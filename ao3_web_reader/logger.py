import logging
import os
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self,
                 logs_filename: str,
                 logs_path: str,
                 backup_log_files_count: int = 7,
                 debug: bool = False,
                 logger_name: str | None = None):

        self.debug_mode = debug

        self.backup_log_files_count = backup_log_files_count

        self.logs_path = self.__set_logs_path(logs_filename, logs_path)
        self.__logger = logging.getLogger(__name__ if logger_name is None else logger_name)

        self.__setup()

    def __set_logs_path(self, filename: str, path: str) -> str:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        return os.path.join(path, filename)

    def __setup(self):
        if self.debug_mode:
            self.__logger.setLevel("DEBUG")
        else:
            self.__logger.setLevel("INFO")

        self.__setup_serial()

        if self.logs_path is not None:
            self.__setup_file()

    def __setup_serial(self):
        formatter = self.__get_formatter(with_day=False)

        console_logger = logging.StreamHandler()
        console_logger.setFormatter(formatter)

        self.__logger.addHandler(console_logger)

    def __setup_file(self):
        formatter = self.__get_formatter()

        file_handler = TimedRotatingFileHandler(filename=self.logs_path,
                                                when="midnight",
                                                encoding="utf-8",
                                                backupCount=self.backup_log_files_count)
        file_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)

    def __get_formatter(self, with_day: bool = True) -> logging.Formatter:
        format = "%Y-%m-%d %H:%M:%S" if with_day else "%H:%M:%S"

        formatter = logging.Formatter(
            "{asctime} - {name} - {levelname} - {message}",
            style="{",
            datefmt=format,
        )

        return formatter

    def exception(self, message: str):
        self.__logger.exception(message)

    def error(self, message: str):
        self.__logger.error(message)

    def info(self, message: str):
        self.__logger.info(message)

    def warning(self, message: str):
        self.__logger.warning(message)

    def debug(self, message: str):
        self.__logger.debug(message)
