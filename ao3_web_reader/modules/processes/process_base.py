import threading
from datetime import datetime
from ao3_web_reader.consts import ProcessesConsts


class ProcessBase:
    def __init__(self, app, owner_id):
        self.app = app
        self.owner_id = owner_id

        self.process = threading.Thread(target=self.mainloop)

        self.timestamp = str(datetime.timestamp(datetime.now()))

    def start_process(self):
        self.app.logger.info(f"starting {self.get_process_name()}")
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

        self.app.processes_manager.set_process_data(self.timestamp, process_data)

    def finish_process(self):
        self.app.processes_manager.remove_process_data(self.timestamp)
