from flask import Blueprint, render_template, flash, abort, redirect, url_for, current_app
import flask_login
from ao3_web_reader.app_modules import forms
from ao3_web_reader.consts import FlashConsts, MessagesConsts
from ao3_web_reader.utils import db_utils
from ao3_web_reader import models
from ao3_web_reader.app_modules.scrapper_process import ScrapperProcess


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/")
@flask_login.login_required
def all_works():
    user_works = models.Work.query.filter_by(owner_id=flask_login.current_user.id).all()

    return render_template("works.html", works=user_works)


@works.route("/<work_id>")
@flask_login.login_required
def management(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        return render_template("management.html", work=user_work)

    else:
        abort(404)


@works.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_work():
    add_work_form = forms.AddWorkForm()

    if add_work_form.validate_on_submit():
        ScrapperProcess(flask_login.current_user.id, current_app, add_work_form.work_id.data).start_process()

        flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

        return redirect(url_for("works.add_work"))

    return render_template("add_work.html", add_work_form=add_work_form)


@works.route("/<work_id>/remove", methods=["POST"])
@flask_login.login_required
def remove_work(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        db_utils.remove_object_from_db(user_work)

        flash(MessagesConsts.WORK_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works"))

    else:
        abort(404)


@works.route("/<work_id>/chapters")
@flask_login.login_required
def chapters(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        return render_template("chapters.html", work=user_work)

    else:
        abort(404)


@works.route("/<work_id>/chapters/<chapter_id>")
@flask_login.login_required
def chapter(work_id, chapter_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        work_chapter = models.Chapter.query.filter_by(work_id=user_work.id, chapter_id=chapter_id).first()

        if work_chapter:
            return render_template("chapter.html", chapter=work_chapter)

    abort(404)
