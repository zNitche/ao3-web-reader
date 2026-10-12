class ValidationConsts:
    pass


class FlashConsts:
    DANGER = "danger"
    SUCCESS = "success"


class MessagesConsts:
    LOGIN_ERROR = "Wrong username or password"
    SCRAPING_PROCESS_STARTED = "Started work scraping"
    CHAPTER_SCRAPING_PROCESS_STARTED = "Started chapter scraping"
    CHAPTERS_UPDATE_PROCESS_STARTED = "Started work update"
    TAG_UPDATE_PROCESS_STARTED = "Started works update"
    SCRAPING_PROCESS_FOR_WORK_ID_RUNNING = "Scraper process for {work_id} is running"
    CANT_ACCESS_WORK = "Can't access work"
    WORK_ALREADY_ADDED = "Work already added"
    WORK_REMOVED = "Work removed successfully"
    TAG_ALREADY_ADDED = "Tag already added"
    ADDED_TAG = "New tag has been added: {tag_name}"
    TAG_DOESNT_EXIST = "Tag doesn't exist"
    TAG_REMOVED = "Tag removed"
    CHAPTERS_MARKED_AS_COMPLETED = "All chapters of '{work_name}' marked as completed"
    CHAPTERS_MARKED_AS_INCOMPLETE = "All chapters of '{work_name}' marked as incomplete"
    WORK_ADDED_TO_FAVORITES = "{work_name} added to favorites"
    WORK_REMOVED_FROM_FAVORITES = "{work_name} removed from favorites"


class PaginationConsts:
    UPDATE_MESSAGES_PER_PAGE = 50
    WORKS_PER_PAGE = 10


class ProcessesConsts:
    PID = "pid"
    OWNER_ID = "owner_id"
    WORK_ID = "work_id"
    CHAPTER_ID = "chapter_id"
    WORK_TITLE = "work_title"
    PROCESS_NAME = "process_name"
    PROGRESS = "progress"

    IS_RUNNING = "is_running"


class UpdateMessagesConsts:
    MESSAGE_ADDED_TYPE = "added"
    MESSAGE_REMOVED_TYPE = "removed"
