class AppManagerBase:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_name():
        return None

    def setup(self):
        pass
