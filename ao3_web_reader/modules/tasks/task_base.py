import threading, os
from datetime import datetime
from ao3_web_reader.consts import ProcessesConsts
from ao3_web_reader import processes_manager
from ao3_web_reader.logger import Logger
from config import Config


class ProcessTask:
    def __init__(self, owner_id):
        self.owner_id = owner_id

        self.process = threading.Thread(target=self.mainloop)

        self.timestamp = str(int(datetime.timestamp(datetime.now())))

        self.process_name = self.__class__.__name__
        self.unique_process_name = f"{self.process_name}_{self.owner_id}_{self.timestamp}"

        self.logger = Logger(logger_name=self.unique_process_name,
                             logs_filename=f"{self.__class__.__name__}.log",
                             logs_path=os.path.join(Config.LOGS_DIR_PATH, "tasks"),
                             backup_log_files_count=1)

    def start_process(self):
        self.logger.info(f"starting")
        self.process.start()

    def mainloop(self):
        pass

    def update_process_data(self):
        process_data = {
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.process_name,
        }

        processes_manager.set_process_data(self.unique_process_name, process_data)

    def finish_process(self):
        processes_manager.remove_process_data(self.unique_process_name)
        self.logger.info("task completed")
