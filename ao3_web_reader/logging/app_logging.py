from flask import Flask
from flask.logging import create_logger
from ao3_web_reader.logging import common


class AppLogging:
    def __init__(self,
                 app: Flask,
                 logs_filename: str | None = None,
                 logs_path: str | None = None,
                 backup_log_files_count: int = 7):

        self.app = app

        self.backup_log_files_count = backup_log_files_count

        self.logs_path = common.set_logs_path(logs_filename, logs_path)
        self.__logger = create_logger(app)

    def setup(self):
        # clear built in logging handlers
        self.__logger.handlers.clear()

        common.setup(logger=self.__logger, logs_path=self.logs_path,
                     is_debug=self.app.debug, backup_log_files_count=self.backup_log_files_count)
