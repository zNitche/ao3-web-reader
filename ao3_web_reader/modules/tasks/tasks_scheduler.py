from ao3_web_reader.modules import CacheDatabase
from ao3_web_reader.logging import Logger
import os, time
from dataclasses import dataclass


@dataclass
class Job():
    uuid: str


class TasksScheduler():
    def __init__(self, cache_db_server_address: str,
                 cache_db_server_port: int,
                 queue_db_id: int, processes_db_id: int,
                 tasks_queue_size: int = 20, workers_count: int = 2) -> None:

        self.__is_running: bool = False

        self.__tasks_queue_size: int = tasks_queue_size
        self.__workers_count: int = workers_count

        self.__cache_db_server_address: str = cache_db_server_address
        self.__cache_db_server_port: int = cache_db_server_port

        self.__queue_db: CacheDatabase = CacheDatabase(queue_db_id)
        self.__processes_db: CacheDatabase = CacheDatabase(processes_db_id)

        self.__logger = Logger()

    def setup(self, logs_path: str) -> None:
        self_name = self.__class__.__name__

        self.__logger = Logger.get_logger(logger_name=self_name,
                                          logs_filename=f"{self_name}.log",
                                          logs_path=os.path.join(
                                              logs_path, "tasks_scheduler"),
                                          backup_log_files_count=2)

        self.__init_cache_dbs()

        self.__logger.info("setup has been completed")

    def __init_cache_dbs(self) -> None:
        self.__queue_db.setup(server_address=self.__cache_db_server_address,
                              server_port=self.__cache_db_server_port, flush=True)

        self.__processes_db.setup(server_address=self.__cache_db_server_address,
                                  server_port=self.__cache_db_server_port, flush=True)

    def start(self) -> None:
        self.__is_running = True
        self.__logger.info("starting mainloop")

        try:
            self.__mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.__is_running = False
            self.__logger.info("exiting")

        except:
            self.__logger.exception("events loop error")

    def __mainloop(self) -> None:
        while self.__is_running:
            time.sleep(10)

