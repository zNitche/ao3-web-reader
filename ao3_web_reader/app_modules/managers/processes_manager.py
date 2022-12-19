from ao3_web_reader.app_modules.managers.app_manager_base import AppManagerBase


class ProcessesManager(AppManagerBase):
    def __init__(self, app):
        super().__init__(app)

        self.redis_manager = None

    @staticmethod
    def get_name():
        return "processes_manager"

    def setup(self):
        self.redis_manager = self.app.redis_manager

    def get_processes_timestamps(self):
        timestamps = self.redis_manager.get_keys()

        return timestamps

    def get_processes_data(self):
        processes_timestamps = self.get_processes_timestamps()

        processes_data = [self.get_process_data(timestamp) for timestamp in processes_timestamps]

        return processes_data

    def set_process_data(self, timestamp, data):
        self.redis_manager.set_value(timestamp, data)

    def get_process_data(self, timestamp):
        process_data = self.redis_manager.get_value(timestamp)

        return process_data

    def remove_process_data(self, timestamp):
        processes_timestamps = self.get_processes_timestamps()

        if timestamp in processes_timestamps:
            self.redis_manager.delete_key(timestamp)
