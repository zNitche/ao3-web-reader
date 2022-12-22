from ao3_web_reader.app_modules.background_processes.works_updater_process import WorksUpdaterProcess


def start_work_updater_processes(app, users):
    for user in users:
        WorksUpdaterProcess(app, user.id).start_process()
