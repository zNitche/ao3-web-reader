import dotenv
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ao3_web_reader'))

dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR_PATH = os.path.join(CURRENT_DIR, "ao3_web_reader")
    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "database", "migrations")

    LOGS_DIR_PATH = os.path.join(CURRENT_DIR, "logs")

    APP_PORT = 8000
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = os.getenv("DEBUG", 0)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"

    REDIS_SERVER_ADDRESS = os.getenv("REDIS_SERVER_ADDRESS")
    REDIS_SERVER_PORT = os.getenv("REDIS_SERVER_PORT")

    WORKS_UPDATER_INTERVAL = int(os.getenv("WORKS_UPDATER_INTERVAL", 7200))
