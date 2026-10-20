from ao3_web_reader.modules.background_processes import WorksUpdaterProcess
from ao3_web_reader.logging import Logger
from config import Config


def main():
    logger = Logger.get_logger(logger_name="tasks_scheduler",
                               logs_filename="tasks_scheduler.log",
                               logs_path=Config.LOGS_DIR_PATH,
                               backup_log_files_count=1)

    processes = [WorksUpdaterProcess]

    try:
        pass

    except Exception as e:
        logger.exception(f"failed to start background process: {str(e)}")


if __name__ == '__main__':
    main()
