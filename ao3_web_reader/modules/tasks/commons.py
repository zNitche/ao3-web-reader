from ao3_web_reader.modules.tasks import types
from typing import Any


def parse_tasks(raw_data: list[tuple[str, dict[str, Any]]]) -> list[types.Task]:
    tasks = []

    for val in raw_data:
        key, raw_task_body = val

        parsed_key = types.Task.parse_cache_db_key(key)
        task_body = types.TaskBody.from_dict(**raw_task_body)

        task = types.Task(
            body=task_body, uuid=parsed_key["uuid"],
            owner_id=parsed_key["owner_id"],
            priority=parsed_key["priority"])

        tasks.append(task)

    return tasks
