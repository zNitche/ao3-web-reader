from flask import current_app
from ao3_web_reader.modules import CacheDatabase
from ao3_web_reader.modules.tasks import types, commons


class TasksManager():
    def __init__(self) -> None:
        self.__tasks_queue_size: int
        self.__queue_db: CacheDatabase

    def setup(self):
        if not current_app:
            raise Exception("used outside flask app context")

        self.__tasks_queue_size = current_app.config["TASKS_QUEUE_SIZE"]
        self.__queue_db = CacheDatabase(
            current_app.config["TASKS_QUEUE_CACHE_DB_ID"])

        cache_db_address: str = current_app.config["WHIMDB_SERVER_ADDRESS"]
        cache_db_port: int = current_app.config["WHIMDB_SERVER_PORT"]

        self.__queue_db.setup(server_address=cache_db_address, server_port=cache_db_port,
                              flush=True)

        current_app.logger.info("ProcessesManager setup has been completed")

    def add_task_to_queue(self, task_body: types.TaskBody, owner_id: int | None = None,
                          priority: types.TaskPriorityEnum = types.TaskPriorityEnum.Medium) -> None:
        task = types.Task(body=task_body, owner_id=owner_id, priority=priority)
        self.__internal_add_task_to_queue(task)

    def __internal_add_task_to_queue(self, task: types.Task) -> None:
        if self.__queue_db.count_db_keys() + 1 > self.__tasks_queue_size:
            raise Exception(f"failed to add {task.uuid}, queue is full")

        key_for_task = task.generate_cache_db_key()
        self.__queue_db.set_value(
            key=key_for_task, value=task.body.to_dict(), ttl=(20 * 60))

    def get_tasks(self) -> list[types.Task]:
        raw_values = self.__queue_db.get_items()
        return commons.parse_tasks(raw_values)

    def remove_task_from_queue(self, uuid: str) -> None:
        re_pattern = types.Task.get_re_pattern_for_key(uuid)
        key = self.__queue_db.get_key_for_pattern(pattern=re_pattern)
        self.__queue_db.delete_key(key=key)
