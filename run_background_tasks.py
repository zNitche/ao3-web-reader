from ao3_web_reader.modules.background_processes import WorksUpdaterProcess
from ao3_web_reader.logging import Logger
from config import Config


def main():
    logger = Logger.get_logger(logger_name="background_tasks_runner",
                               logs_filename="background_tasks.log",
                               logs_path=Config.LOGS_DIR_PATH,
                               backup_log_files_count=1)

    processes = [WorksUpdaterProcess]

    for process in processes:
        try:
            instance = process()

            logger.info(f"starting {instance.get_process_name()}...")
            instance.start_process()

            logger.info(f"{instance.get_process_name()} has been started")

        except Exception as e:
            logger.exception(f"failed to start background process: {str(e)}")


if __name__ == '__main__':
    main()
