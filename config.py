import os


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR_PATH = os.path.join(CURRENT_DIR, "ao3_web_reader")
    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "migrations")

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"
