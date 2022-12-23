from ao3_web_reader.models import User
from config import Config
from werkzeug.security import generate_password_hash
import sqlalchemy
import sqlalchemy.orm
import os


class UsersManager:
    def __init__(self):
        self.db_session = None
        self.modules = []

        self.init_modules()
        self.init_db_session()

    def init_modules(self):
        from users_manager.modules.module_base import ModuleBase
        from users_manager.modules.show_users_module import ShowUsersModule
        from users_manager.modules.add_user_module import AddUserModule
        from users_manager.modules.remove_user_module import RemoveUserModule
        from users_manager.modules.reset_user_password_module import ResetUserPasswordModule
        from users_manager.modules.exit_module import ExitModule

        self.modules = [module(self) for module in ModuleBase.__subclasses__()]

    def get_users_names(self):
        names = []

        with self.db_session() as session:
            users = session.query(User).all()

            for user in users:
                names.append(user.username)

        return names

    def hash_password(self, plain_password):
        password = generate_password_hash(plain_password)

        return password

    def init_db_session(self):
        engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)

        self.db_session = sqlalchemy.orm.sessionmaker(engine)

    def add_user(self, user_name, password):
        if user_name in self.get_users_names():
            return False

        encrypted_password = self.hash_password(password)

        user = User(username=user_name, password=encrypted_password)

        with self.db_session() as session:
            session.add(user)
            session.commit()

        return True

    def delete_user(self, user_name):
        with self.db_session() as session:
            user = session.query(User).filter_by(username=user_name).first()

            if user:
                session.delete(user)
                session.commit()

            else:
                return False

            return True

    def reset_user_password(self, user_name, password):
        with self.db_session() as session:
            user = session.query(User).filter_by(username=user_name).first()

            if not user:
                return False

            encrypted_password = self.hash_password(password)

            user.password = encrypted_password

            session.commit()

        return True

    def mainloop(self):
        print("---Users Manager---")
        print("Choose what do you want to do: ")

        for id, module in enumerate(self.modules):
            print(f"{id}) {module.name}")

        choice = int(input("> "))
        os.system("clear")

        if 0 <= choice < len(self.modules):
            module = self.modules[choice]

            module.show()
            module.action()

        else:
            print("Unknown option")

        input("\nPress any key to continue")

        self.mainloop()
