from flask import Blueprint, Response
from ao3_web_reader import auth_manager
from ao3_web_reader.authentication.decorators import login_required


api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/healthcheck", methods=["GET"])
def healthcheck():
    return Response(status=200)


@api.route("/sync-status", methods=["GET"])
@login_required
def sync_status():
    return {
        "is_running": False,
        "progress": 0
    }


@api.route("/running-scraping-tasks", methods=["GET"])
@login_required
def running_scraping_processes():
    user = auth_manager.current_user()
    running_processes = []

    response = {
        "processes_data": running_processes
    }

    return response
