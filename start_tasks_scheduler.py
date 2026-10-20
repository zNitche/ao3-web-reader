from ao3_web_reader.modules.tasks import TasksScheduler
from config import Config


def main():
    cache_db_address = Config.WHIMDB_SERVER_ADDRESS
    cache_db_port = Config.WHIMDB_SERVER_PORT

    if not cache_db_address or cache_db_address == -1:
        raise Exception("invalid cache database connection details")

    scheduler = TasksScheduler(cache_db_server_address=cache_db_address,
                               cache_db_server_port=cache_db_port,
                               queue_db_id=Config.TASKS_QUEUE_CACHE_DB_ID,
                               processes_db_id=Config.TASKS_PROCESSES_CACHE_DB_ID,
                               workers_count=2)

    scheduler.setup(logs_path=Config.LOGS_DIR_PATH)
    scheduler.start()


if __name__ == '__main__':
    main()
