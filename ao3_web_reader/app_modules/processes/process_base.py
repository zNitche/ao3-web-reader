import multiprocessing
from datetime import datetime
from ao3_web_reader.consts import ProcessesConsts


class ProcessBase:
    def __init__(self, app, owner_id):
        self.app = app
        self.owner_id = owner_id

        self.process = multiprocessing.Process(target=self.mainloop)

        self.timestamp = str(datetime.timestamp(datetime.now()))
        self.process_pid = None

    def get_process_name(self):
        return type(self).__name__

    def mainloop(self):
        pass

    def update_process_data(self):
        process_data = {
            ProcessesConsts.PID: self.process_pid,
            ProcessesConsts.OWNER_ID: self.owner_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
        }

        self.app.processes_manager.set_process_data(self.timestamp, process_data)

    def finish_process(self):
        self.app.processes_manager.remove_process_data(self.timestamp)
