from flask import Blueprint, render_template
import flask_login


main = Blueprint("main", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main.route("/")
@flask_login.login_required
def home():
    return render_template("index.html")
