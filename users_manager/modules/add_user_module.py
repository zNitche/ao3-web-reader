from users_manager.modules.module_base import ModuleBase


class AddUserModule(ModuleBase):
    def __init__(self, manager):
        super().__init__(manager)

        self.name = "Add user"

    def show(self):
        print(f"---{self.name}--")

    def action(self):
        print("Username: ")
        user_name = input("> ")

        print("Password: ")
        password = input("> ")

        check = self.manager.add_user(user_name, password)

        print("User already exists") if not check else print("Added user")
