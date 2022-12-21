from flask import Blueprint, render_template
import flask_login
from ao3_web_reader import models


main = Blueprint("main", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main.route("/")
@flask_login.login_required
def home():
    messages = models.UpdateMessage.query.order_by(models.UpdateMessage.date.desc()).all()

    return render_template("index.html", messages=messages)
