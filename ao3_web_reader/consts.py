class ValidationConsts:
    pass


class FlashConsts:
    DANGER = "danger"
    SUCCESS = "success"


class MessagesConsts:
    LOGIN_ERROR = "Wrong username of password"
    SCRAPING_PROCESS_STARTED = "Started work scraping"
    WORK_DOESNT_EXIST = "Work doesn't exist"
    WORK_ALREADY_ADDED = "Work already added"
    WORK_REMOVED = "Work removed successfully"


class AO3Consts:
    AO3_URL = "https://archiveofourown.org/"
    AO3_WORKS_URL = AO3_URL + "works/{work_id}"
    AO3_WORKS_NAVIGATION_URL = AO3_URL + "works/{work_id}/navigate"


class ProcessesConsts:
    PID = "pid"
    OWNER_ID = "owner_id"
    WORK_ID = "work_id"
    WORK_TITLE = "work_title"
    PROCESS_NAME = "process_name"
