import multiprocessing
import time
import os
from config import Config
from ao3_web_reader.logger import Logger
from ao3_web_reader.db import Database
from ao3_web_reader.modules.managers import RedisClient, ProcessesManager


class BackgroundProcessBase:
    def __init__(self, startup_delay=10):
        self.startup_delay = startup_delay

        self.db = Database()

        self.logger = Logger()

        self.processes_cache = RedisClient(db_id=0)
        self.processes_manager = ProcessesManager(cache_db=self.processes_cache)

        self.process = multiprocessing.Process(target=self._runner)
        self.process_pid = None

    def _setup(self):
        self_name = self.__class__.__name__

        self.logger = Logger(logger_name=self_name,
                             logs_filename=f"{self_name}.log",
                             logs_path=os.path.join(Config.LOGS_DIR_PATH, "background_tasks"),
                             backup_log_files_count=2)

        self.logger.info("setup has been started...")

        cache_db_url = Config.REDIS_SERVER_ADDRESS
        cache_db_port = int(Config.REDIS_SERVER_PORT) if Config.REDIS_SERVER_PORT else None

        self.processes_cache.setup(cache_db_url, cache_db_port, flush=False)

        self.db.setup(Config.DATABASE_URI)
        self.db.create_all()

        self.logger.info("setup done...")

    def start_process(self):
        self.process.start()
        self.process_pid = self.process.pid

    def get_process_name(self):
        return type(self).__name__

    def _runner(self):
        self._setup()
        time.sleep(self.startup_delay)

        self.mainloop()

    def mainloop(self):
        raise NotImplementedError()

    def update_process_data(self, ttl=60):
        self.processes_manager.set_process_data(self.get_process_name(), self.get_process_data(), ttl=ttl)

    def get_process_data(self):
        return {}
