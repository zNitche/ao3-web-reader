import multiprocessing
import time
from config import Config
from ao3_web_reader.db import Database
from ao3_web_reader.modules.managers import RedisClient, ProcessesManager


class BackgroundProcessBase:
    def __init__(self, startup_delay=10):
        self.startup_delay = startup_delay

        self.db = Database()

        self.processes_cache = RedisClient(db_id=0)
        self.processes_manager = ProcessesManager(cache_db=self.processes_cache)

        self.process = multiprocessing.Process(target=self.__runner)
        self.process_pid = None

    def _setup(self):
        cache_db_url = Config.REDIS_SERVER_ADDRESS
        cache_db_port = int(Config.REDIS_SERVER_PORT)

        self.processes_cache.setup(cache_db_url, cache_db_port, flush=False)

        self.db.setup(Config.DATABASE_URI)
        self.db.create_all()

    def start_process(self):
        self.process_handler()

        self.process.start()
        self.process_pid = self.process.pid

    def process_handler(self):
        pass

    def get_process_name(self):
        return type(self).__name__

    def __runner(self):
        self._setup()
        time.sleep(self.startup_delay)

        self.mainloop()

    def mainloop(self):
        raise NotImplementedError()

    def update_process_data(self):
        self.processes_manager.set_process_data(self.get_process_name(), self.get_process_data())

    def get_process_data(self):
        return {}
