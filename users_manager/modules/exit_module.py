from users_manager.modules.module_base import ModuleBase
import sys


class ExitModule(ModuleBase):
    def __init__(self, manager):
        super().__init__(manager)

        self.name = "Exit"

    def action(self):
        sys.exit()
