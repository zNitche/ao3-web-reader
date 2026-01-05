from ao3_web_reader import Config


class TestConfig(Config):
    TESTING = True
    DEBUG_MODE = False
    DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    WHIMDB_SERVER_ADDRESS = "127.0.0.1"
    WHIMDB_SERVER_PORT = "6000"
