from users_manager.modules.module_base import ModuleBase


class ResetUserPasswordModule(ModuleBase):
    def __init__(self, manager):
        super().__init__(manager)

        self.name = "Reset user password"

    def show(self):
        print(f"---{self.name}--")

    def action(self):
        print("Username: ")
        user_name = input("> ")

        print("Password: ")
        password = input("> ")

        check = self.manager.reset_user_password(user_name, password)

        print("User doesn't exist") if not check else print("Done")
