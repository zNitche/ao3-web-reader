from users_manager.modules.module_base import ModuleBase


class RemoveUserModule(ModuleBase):
    def __init__(self, manager):
        super().__init__(manager)

        self.name = "Remove user"

    def show(self):
        print(f"---{self.name}--")

    def action(self):
        print("Username: ")
        user_name = input("> ")

        check = self.manager.delete_user(user_name)

        print("User doesn't exist") if not check else print("Removed user")
