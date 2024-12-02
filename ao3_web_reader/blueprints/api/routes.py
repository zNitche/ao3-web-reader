from flask import Blueprint, Response, abort
from ao3_web_reader import processes_manager, auth_manager, models
from ao3_web_reader.authentication.decorators import login_required
from ao3_web_reader.consts import ProcessesConsts


api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response(status=200)


@api.route("/sync-status", methods=["GET"])
@login_required
def sync_status():
    sync_process_status = processes_manager.get_background_process_data("WorksUpdaterProcess")
    sync_process_running = True if sync_process_status and sync_process_status.get(ProcessesConsts.IS_RUNNING) else False

    return {
        "is_running": sync_process_running,
        "progress": sync_process_status.get(ProcessesConsts.PROGRESS) if sync_process_status else 0,
    }


@api.route("/running-scraping-tasks", methods=["GET"])
@login_required
def running_scraping_processes():
    user = auth_manager.current_user()
    running_processes = processes_manager.get_processes_data_for_user("ScraperTask", user.id)

    response = {
        "processes_data": running_processes
    }

    return response

@api.route("/<tag_name>/all-works", methods=["GET"])
@login_required
def tag_all_works(tag_name):
    user = auth_manager.current_user()
    tag = models.Tag.query.filter_by(name=tag_name, owner_id=user.id).first()

    if tag is None:
        abort(404)

    return [{
        "name": work.name,
        "work_id": work.work_id,
        "id": work.id,
    } for work in tag.works]
