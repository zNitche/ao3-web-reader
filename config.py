from load_dotenv import load_dotenv
from datetime import timedelta
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'ao3_web_reader'))

load_dotenv(".env")


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR_PATH = os.path.join(CURRENT_DIR, "ao3_web_reader")
    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "database", "migrations")

    LOGS_DIR_PATH = os.path.join(CURRENT_DIR, "logs")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = bool(int(os.getenv("HTTPS_ONLY", 1)))
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    APP_PORT = 8000
    APP_HOST = "0.0.0.0"

    STYLES_LIBS_FROM_CDN = int(os.getenv("STYLES_LIBS_FROM_CDN", 0))
    DEBUG_MODE = os.getenv("DEBUG", 0)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_URI = f"sqlite:////{CURRENT_DIR}/database/app.db"

    WHIMDB_SERVER_ADDRESS = os.getenv("WHIMDB_SERVER_ADDRESS")
    WHIMDB_SERVER_PORT = os.getenv("WHIMDB_SERVER_PORT")

    WORKS_UPDATER_INTERVAL = int(os.getenv("WORKS_UPDATER_INTERVAL", 7200))
