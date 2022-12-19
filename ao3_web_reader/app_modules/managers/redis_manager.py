import redis
import json
from contextlib import contextmanager
from ao3_web_reader.app_modules.managers.app_manager_base import AppManagerBase
from config import Config


class RedisManager(AppManagerBase):
    def __init__(self, app, db_id):
        super().__init__(app)

        self.server_address = Config.REDIS_SERVER_ADDRESS
        self.server_port = int(Config.REDIS_SERVER_PORT)
        self.db_id = db_id

        self.connection_pool = None

    @staticmethod
    def get_name():
        return "redis_manager"

    @contextmanager
    def db_connection(self, raise_exception=False):
        try:
            connection = redis.Redis(connection_pool=self.connection_pool)
            yield connection

        except Exception as e:
            if raise_exception:
                raise

    def setup(self):
        self.create_connection_pool()
        self.flush_db()

    def create_connection_pool(self):
        self.connection_pool = redis.ConnectionPool(host=self.server_address, port=self.server_port, db=self.db_id,
                                                    decode_responses=True)

    def flush_db(self):
        with self.db_connection(raise_exception=True) as connection:
            connection.flushdb()

    def set_value(self, key, value):
        with self.db_connection() as connection:
            connection.set(key, json.dumps(value))

    def get_value(self, key):
        value = None

        with self.db_connection() as connection:
            data = connection.get(key)

        if data:
            value = json.loads(data)

        return value

    def get_keys(self):
        with self.db_connection() as connection:
            keys = connection.scan_iter("*")

        return keys

    def delete_key(self, key):
        with self.db_connection() as connection:
            connection.delete(key)
