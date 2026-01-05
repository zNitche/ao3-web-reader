from whimdb import Client
import json


class CacheDatabase:
    def __init__(self, db_id: int):
        self.db_id: int = db_id

        self.__client: Client | None = None

    @property
    def client(self):
        if not self.__client:
            raise Exception("database hasn't been setup yet, client is None")

        return self.__client

    def setup(self, server_address: str, server_port: int, flush: bool = False):
        self.__client = Client(addr=server_address,
                               port=server_port, database_id=self.db_id)

        if flush:
            self.flush_db()

    def flush_db(self):
        self.client.purge()

    def __query_single_item(self, key: str | None = None, search_regex: str | None = None):
        res = self.client.query(key=key, search_regex=search_regex)

        if not res or not res.value:
            return None

        if len(res.value) == 0:
            return None

        return res.value[0]

    def update_ttl(self, key: str, ttl: int):
        self.client.update_ttl(key=key, ttl=ttl)

    def get_ttl(self, key: str) -> int | None:
        item = self.__query_single_item(key)

        if not item:
            return None

        return item.ttl_left

    def set_value(self, key: str, value: dict | str | int | bool, ttl=60):
        self.client.set(key=key, value=json.dumps(value), ttl=ttl)

    def get_value(self, key: str | None = None, pattern: str | None = None):
        item = self.__query_single_item(key, search_regex=pattern)

        return json.loads(item.value) if item else None
    
    def get_keys(self):
        data = self.client.query(search_regex="(.*?)")

        if not data or not data.value:
            return []

        return [item.key for item in data.value]

    def get_key_for_pattern(self, pattern: str) -> str | None:
        item = self.__query_single_item(search_regex=pattern)

        if not item or not item.value:
            return None

        return item.key

    def get_all_keys_for_pattern(self, pattern: str):
        keys = []

        for page in self.client.query_pages(search_regex=pattern):
            if not page:
                break

            for item in page:
                keys.append(item.key)

        return keys

    def delete_key(self, key: str | None = None, pattern: str | None = None):
        if key is not None:
            self.client.remove(key=key)
            return

        if pattern is not None:
            keys_to_remove = self.get_all_keys_for_pattern(pattern)

            for key_to_remove in keys_to_remove:
                self.client.remove(key=key_to_remove)
