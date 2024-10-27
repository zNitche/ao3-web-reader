import flask_login
from flask import Blueprint, current_app, Response
from ao3_web_reader.consts import ProcessesConsts
from flask_login import login_required


api = Blueprint("api", __name__, template_folder="templates", static_folder="static", url_prefix="/api")


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response(status=200)


@api.route("/sync-status", methods=["GET"])
@login_required
def sync_status():
    sync_process_status = current_app.processes_manager.get_background_process_data("WorksUpdaterProcess")
    sync_process_running = True if sync_process_status and sync_process_status.get(ProcessesConsts.IS_RUNNING) else False

    return {
        "is_running": sync_process_running,
        "progress": sync_process_status.get(ProcessesConsts.PROGRESS) if sync_process_status else 0,
    }


@api.route("/running-scraping-processes", methods=["GET"])
@login_required
def running_scraping_processes():
    user_id = flask_login.current_user.id
    running_processes = current_app.processes_manager.get_processes_data_for_user("ScraperProcess", user_id)

    response = {
        "processes_data": running_processes
    }

    return response
