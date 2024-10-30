import redis
import json
from contextlib import contextmanager


class RedisClient:
    def __init__(self, db_id):
        self.server_address = None
        self.server_port = None
        self.db_id = db_id

        self.connection_pool = None

    @contextmanager
    def db_session(self, raise_exception=False):
        connection = redis.Redis(connection_pool=self.connection_pool)

        try:
            yield connection

        except Exception as e:
            if raise_exception:
                raise

        finally:
            connection.close()

    def setup(self, address, port):
        self.server_address = address
        self.server_port = port

        self.create_connection_pool()
        self.flush_db()

    def create_connection_pool(self):
        self.connection_pool = redis.ConnectionPool(host=self.server_address, port=self.server_port, db=self.db_id,
                                                    decode_responses=True)

    def flush_db(self):
        with self.db_session(raise_exception=True) as session:
            session.flushdb()

    def set_value(self, key, value, ttl=30):
        with self.db_session() as session:
            session.set(key, json.dumps(value), ex=ttl)

    def get_value(self, key):
        with self.db_session() as session:
            data = session.get(key)

        return json.loads(data) if data else None

    def get_keys(self):
        with self.db_session() as session:
            keys = session.scan_iter("*")

        return keys

    def delete_key(self, key):
        with self.db_session() as session:
            session.delete(key)
