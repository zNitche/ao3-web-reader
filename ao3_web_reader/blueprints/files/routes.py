from flask import Blueprint, render_template
from ao3_web_reader.authentication.decorators import login_required


files = Blueprint("files", __name__, template_folder="templates", static_folder="static", url_prefix="/files")


@files.route("/")
@login_required
def all():
    return render_template("all.html")
