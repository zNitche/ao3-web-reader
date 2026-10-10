from enum import Enum
from ao3_web_reader.modules.managers import CacheDatabase
from uuid import uuid4
import json
from dataclasses import dataclass


class MessageType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class MessageData:
    type: str
    text: str


class MessagingManager():
    def __init__(self, cache_db: CacheDatabase, message_ttl: int = 300) -> None:
        self.__cache_db = cache_db
        self.__message_ttl = message_ttl

    def __generate_key(self, type: MessageType | None = None, user_id: int | None = None):
        key = str(uuid4())
        key = f"{type.value}_{key}" if type != None else key
        key = f"{user_id}_{key}" if user_id != None else key
        return key

    def add_message(self, type: MessageType, message: str, user_id: int | None = None):
        key = self.__generate_key(type=type, user_id=user_id)
        message_data = MessageData(text=message, type=type.value)

        self.__cache_db.set_value(
            key=key, value=message_data.__dict__, ttl=self.__message_ttl)

    def get_messages(self, type: MessageType | None, user_id: int,
                     remove_on_get: bool = False) -> list[MessageData]:

        pattern = f"^{user_id}_{type.value}_.+$" if type != None else f"^{user_id}_.+$"

        vals = self.__cache_db.get_values_for_pattern(
            pattern=pattern)

        if len(vals) > 0 and remove_on_get:
            keys = self.__cache_db.get_all_keys_for_pattern(
                pattern=pattern)

            for key in keys:
                self.__cache_db.delete_key(key=key)

        messages: list[MessageData] = [
            MessageData(**json.loads(val)) for val in vals
        ]

        return messages
