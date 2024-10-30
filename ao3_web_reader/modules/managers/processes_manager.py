from ao3_web_reader.consts import ProcessesConsts


class ProcessesManager:
    def __init__(self, cache_db):
        self.cache_manager = cache_db

    def get_processes_timestamps(self):
        timestamps = self.cache_manager.get_keys()

        return timestamps

    def get_processes_data(self, process_type=None):
        processes_timestamps = self.get_processes_timestamps()
        processes_data = []

        for timestamp in processes_timestamps:
            data = self.get_process_data(timestamp, process_type)

            if data is not None:
                processes_data.append(data)

        return processes_data

    def get_processes_data_for_user(self, process_type, user_id):
        all_processes_data = self.get_processes_data(process_type)
        processes_data = [data for data in all_processes_data if data.get(ProcessesConsts.OWNER_ID) == user_id]

        return processes_data

    def get_processes_data_for_user_and_work(self, process_type, user_id, work_id):
        all_processes_data = self.get_processes_data(process_type)
        processes_data = [data for data in all_processes_data
                          if data.get(ProcessesConsts.OWNER_ID) == user_id and
                          data.get(ProcessesConsts.WORK_ID) == work_id]

        return processes_data

    def get_processes_data_for_user_and_chapter(self, process_type, user_id, chapter_id):
        all_processes_data = self.get_processes_data(process_type)
        processes_data = [data for data in all_processes_data
                          if data.get(ProcessesConsts.OWNER_ID) == user_id and
                          data.get(ProcessesConsts.CHAPTER_ID) == chapter_id]

        return processes_data

    def set_process_data(self, timestamp, data):
        self.cache_manager.set_value(timestamp, data)

    def get_process_data(self, timestamp, process_type=None):
        process_data = self.cache_manager.get_value(timestamp)

        if process_type is not None and process_data.get(ProcessesConsts.PROCESS_NAME) != process_type:
            process_data = None

        return process_data

    def set_background_process_data(self, process_name, data):
        self.cache_manager.set_value(process_name, data)

    def get_background_process_data(self, process_name):
        process_data = self.cache_manager.get_value(process_name)

        return process_data

    def remove_process_data(self, timestamp):
        processes_timestamps = self.get_processes_timestamps()

        if timestamp in processes_timestamps:
            self.cache_manager.delete_key(timestamp)
