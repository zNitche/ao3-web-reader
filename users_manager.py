from ao3_web_reader.models import User
from config import Config
from werkzeug.security import generate_password_hash
import sqlalchemy
import sqlalchemy.orm
import os


class UsersManager:
    def __init__(self):
        self.db_session = None
        self.users_names = []

        self.init_db_session()
        self.get_users_names()

    def get_users_names(self):
        with self.db_session() as session:
            users = session.query(User).all()

            for user in users:
                self.users_names.append(user.username)

    def hash_password(self, plain_password):
        password = generate_password_hash(plain_password)

        return password

    def init_db_session(self):
        engine = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)

        self.db_session = sqlalchemy.orm.sessionmaker(engine)

    def add_user(self, user_name, password):
        if user_name in self.users_names:
            return 0

        encrypted_password = self.hash_password(password)

        user = User(username=user_name, password=encrypted_password)

        with self.db_session() as session:
            session.add(user)
            session.commit()

        return 1

    def delete_user(self, user_name):
        with self.db_session() as session:
            user = session.query(User).filter_by(username=user_name).first()

            if user:
                session.delete(user)
                session.commit()

            else:
                return 0

            return 1


def show_users(users):
    for user_name in users:
        print(user_name)


def conv_string_to_bool(s):
    if s == "true" or s == "True":
        return True

    elif s == "false" or s == "False":
        return False


def main():
    manager = UsersManager()

    print("---Users Manager---")
    print("Choose what do you want to do: ")
    print("1) Add new user")
    print("2) Delete user")
    print("3) Show users")
    print("4) Exit")

    choice = int(input("> "))
    os.system("clear")

    if choice == 1:
        print("---Add user---")

        print("Username: ")
        user_name = input("> ")

        print("Password: ")
        password = input("> ")

        check = manager.add_user(user_name, password)

        print("User already exists") if not check else print("Added user")

        input("\nPress any key to continue")

        main()

    elif choice == 2:
        print("---Delete user---")

        print("Username: ")
        user_name = input("> ")

        check = manager.delete_user(user_name)

        print("User doesn't exist") if not check else print("Removed user")

        input("\nPress any key to continue")

        main()

    elif choice == 3:
        show_users(manager.users_names)

        input("\nPress any key to continue")

        main()

    elif choice == 4:
        return

    else:
        print("Unknown option")
        input("\nPress any key to continue")

        main()


if __name__ == '__main__':
    main()
