from users_manager.modules.module_base import ModuleBase


class ShowUsersModule(ModuleBase):
    def __init__(self, manager):
        super().__init__(manager)

        self.name = "Show users"

    def show(self):
        print(f"---{self.name}--")

    def action(self):
        for name in self.manager.get_users_names():
            print(name)
