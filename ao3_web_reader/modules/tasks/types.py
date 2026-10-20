from typing import Any
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from ao3_web_reader.modules.types import mixins


class TaskPriorityEnum(Enum):
    High = 1
    Medium = 2
    Low = 3


@dataclass
class TaskBody(mixins.SerializableObjectMixin):
    runner: str


@dataclass
class Task():
    body: TaskBody
    uuid: str = field(default_factory=lambda: str(uuid4()))
    owner_id: int | None = None
    priority: TaskPriorityEnum = TaskPriorityEnum.Medium

    @staticmethod
    def get_re_pattern_for_key(uuid: str) -> str:
        return f"^{uuid}_.+$"

    @staticmethod
    def parse_cache_db_key(key: str) -> dict[str, Any]:
        split_key = key.split("_")

        return {
            "uuid": split_key[0],
            "priority": TaskPriorityEnum(int(split_key[1])),
            "owner_id": None if split_key[2] == "None" else split_key[2]
        }

    def generate_cache_db_key(self) -> str:
        return f"{self.uuid}_{self.priority}_{self.owner_id}"
