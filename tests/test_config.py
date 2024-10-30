class TestConfig:
    TESTING = True
    DEBUG_MODE = False
    DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    REDIS_SERVER_ADDRESS = "127.0.0.1"
    REDIS_SERVER_PORT = "6000"
