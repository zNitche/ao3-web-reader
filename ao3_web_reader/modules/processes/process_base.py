import threading, os
from datetime import datetime
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import processes_manager
from ao3_web_reader.logger import Logger
from config import Config


class ProcessBase:
    def __init__(self, owner_id):
        self.owner_id = owner_id

        self.process = threading.Thread(target=self.mainloop)

        self.timestamp = str(datetime.timestamp(datetime.now()))

        self.logger = Logger(logger_name=f"{self.__class__.__name__}_{self.timestamp}",
                             logs_filename=f"{self.__class__.__name__}.log",
                             logs_path=os.path.join(Config.LOGS_DIR_PATH, "tasks"),
                             backup_log_files_count=1)

    def start_process(self):
        self.logger.info(f"starting")
        self.process.start()

    def get_process_name(self):
        return type(self).__name__

    def mainloop(self):
        pass

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
        }

        processes_manager.set_process_data(self.timestamp, process_data)

    def finish_process(self):
        processes_manager.remove_process_data(self.timestamp)
        self.logger.info("task completed")
