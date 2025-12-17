import os


def load_dotenv(file_path: str):
    if not os.path.exists(file_path):
        raise Exception(
            f".env file loading has failed, {file_path} doesn't exist")

    with open(file_path, "r") as file:
        lines = file.readlines()

        for line in lines:
            split_line = line.split("=")

            if len(split_line) == 2:
                name, value = split_line
                os.environ[name] = value.rstrip()
