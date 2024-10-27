from flask import Blueprint, render_template
import flask_login


files = Blueprint("files", __name__, template_folder="templates", static_folder="static", url_prefix="/files")


@files.route("/")
@flask_login.login_required
def all():
    return render_template("all.html")
