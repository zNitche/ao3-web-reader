from typing import Any
import logging
from ao3_web_reader.logging import common
from ao3_web_reader.logging.adapters import ExtendableLogsAdapter


class Logger:
    def __init__(self):
        # set via init() method
        self.debug_mode = False

        self.log_to_file = None
        self.backup_log_files_count = 7
        self.logs_path = None

        self.__logger: logging.Logger | None = None

    def init(self,
             logger_name: str | None = None,
             debug: bool = False,
             log_to_file: bool = False,
             logs_filename: str | None = None,
             logs_path: str | None = None,
             backup_log_files_count: int | None = None):

        self.__logger = logging.getLogger(logger_name)

        # already configured
        if self.__logger.handlers:
            return

        self.debug_mode = debug
        self.log_to_file = log_to_file

        self.backup_log_files_count = backup_log_files_count
        self.logs_path = common.set_logs_path(
            filename=logs_filename, path=logs_path)

        self.__setup()

    def __setup(self):
        if self.__logger is None:
            raise Exception("can't setup None logger")

        common.setup(logger=self.__logger, logs_path=self.logs_path,
                     is_debug=self.debug_mode, backup_log_files_count=self.backup_log_files_count)

    @staticmethod
    def get_expandable_logger(logger_name: str, extra: dict[str, Any], logs_path: str | None = None,
                              logs_filename: str | None = None, backup_log_files_count: int | None = None):
        logger = Logger()
        logger.init(logger_name=logger_name, logs_filename=logs_filename,
                    backup_log_files_count=backup_log_files_count, logs_path=logs_path)

        return ExtendableLogsAdapter(logger.__logger, extra=extra)

    @staticmethod
    def get_logger(logger_name: str, logs_path: str | None = None,
                   logs_filename: str | None = None, backup_log_files_count: int | None = None):
        logger = Logger()
        logger.init(logger_name=logger_name, logs_filename=logs_filename,
                    backup_log_files_count=backup_log_files_count, logs_path=logs_path)

        return logger

    def exception(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.exception(message)

    def error(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.error(message)

    def info(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.info(message)

    def warning(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.warning(message)

    def debug(self, message: str):
        if not self.__logger:
            raise Exception("logger is None")

        self.__logger.debug(message)
