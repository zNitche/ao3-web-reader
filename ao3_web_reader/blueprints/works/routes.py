from flask import Blueprint, render_template
import flask_login
from ao3_web_reader.app_modules import forms


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/")
@flask_login.login_required
def all_works():
    return render_template("works.html")


@works.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_work():
    add_work_form = forms.AddWorkForm()

    return render_template("add_work.html", add_work_form=add_work_form)


@works.route("/<work_id>/chapters")
@flask_login.login_required
def chapters(work_id):
    return render_template("chapters.html")


@works.route("/<work_id>/chapters/<chapter_id>")
@flask_login.login_required
def chapter(work_id, chapter_id):
    return render_template("chapter.html")
