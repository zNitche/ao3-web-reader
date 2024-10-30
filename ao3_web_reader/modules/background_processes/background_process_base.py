import multiprocessing


class BackgroundProcessBase:
    def __init__(self, app):
        self.app = app

        self.process = multiprocessing.Process(target=self.mainloop)
        self.process_pid = None

    def start_process(self):
        self.app.logger.info(f"starting {self.get_process_name()}")

        self.process_handler()

        self.process.start()
        self.process_pid = self.process.pid

    def process_handler(self):
        pass

    def get_process_name(self):
        return type(self).__name__

    def mainloop(self):
        raise NotImplementedError()

    def update_process_data(self):
        self.app.processes_manager.set_process_data(self.get_process_name(), self.get_process_data())

    def get_process_data(self):
        return {}
