from flask import Blueprint, current_app
from ao3_web_reader.consts import ProcessesConsts


api = Blueprint("api", __name__, template_folder="templates", static_folder="static", url_prefix="/api")


@api.route("/sync_status", methods=["GET"])
def sync_status():
    sync_process_status = current_app.processes_manager.get_background_process_data("WorksUpdaterProcess")
    sync_process_running = True if sync_process_status and sync_process_status.get(ProcessesConsts.IS_RUNNING) else False

    return {
        "is_running": sync_process_running
    }
