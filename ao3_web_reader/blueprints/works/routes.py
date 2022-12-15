from flask import Blueprint, render_template, flash, abort
import flask_login
from ao3_web_reader.app_modules import forms
from ao3_web_reader.consts import FlashConsts, MessagesConsts
from ao3_web_reader.utils import works_utils, db_utils
from ao3_web_reader import models


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/")
@flask_login.login_required
def all_works():
    user_works = models.Work.query.filter_by(owner_id=flask_login.current_user.id).all()

    return render_template("works.html", works=user_works)


@works.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_work():
    add_work_form = forms.AddWorkForm()

    if add_work_form.validate_on_submit():
        work_data = works_utils.get_work(add_work_form.work_id.data)

        work = models.Work(name=work_data["name"], owner_id=flask_login.current_user.id, work_id=work_data["work_id"])

        for chapter_data in work_data["chapters_data"]:
            title = chapter_data["name"]
            content = chapter_data["content"]

            chapter = models.Chapter(title=title)

            for text in content:
                text_row = models.TextRow(content=text)
                chapter.rows.append(text_row)

            work.chapters.append(chapter)

        db_utils.add_object_to_db(work)

        flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

    return render_template("add_work.html", add_work_form=add_work_form)


@works.route("/<work_id>/chapters")
@flask_login.login_required
def chapters(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        return render_template("chapters.html", chapters=user_work.chapters)

    else:
        abort(404)


@works.route("/<work_id>/chapters/<chapter_id>")
@flask_login.login_required
def chapter(work_id, chapter_id):
    return render_template("chapter.html")
