from flask import Blueprint, render_template, flash, abort, redirect, url_for, current_app, send_file
import flask_login
from ao3_web_reader.app_modules import forms
from ao3_web_reader.consts import FlashConsts, MessagesConsts, ProcessesConsts
from ao3_web_reader.utils import db_utils, files_utils
from ao3_web_reader import models
from ao3_web_reader.app_modules.processes.scraper_process import ScraperProcess
import tempfile
import os


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/<tag_name>")
@flask_login.login_required
def all_works(tag_name):
    tag = models.Tag.query.filter_by(owner_id=flask_login.current_user.id, name=tag_name).first()

    if tag:
        works = models.Work.query.filter_by(tag_id=tag.id).order_by(models.Work.last_updated.desc()).all()

        return render_template("works.html", works=works)

    abort(404)


@works.route("/<work_id>/management")
@flask_login.login_required
def management(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        return render_template("management.html", work=user_work)

    abort(404)


@works.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_work():
    add_work_form = forms.AddWorkForm()

    tags = models.Tag.query.filter_by(owner_id=flask_login.current_user.id).all()
    add_work_form.tag_name.choices = [tag.name for tag in tags]

    running_processes = current_app.processes_manager.get_processes_data("ScraperProcess")

    if add_work_form.validate_on_submit():
        work_id = add_work_form.work_id.data
        tag_name = add_work_form.tag_name.data

        running_processes_with_same_work_id = \
            [process for process in running_processes if process[ProcessesConsts.WORK_ID] == work_id]

        if len(running_processes_with_same_work_id) == 0:
            ScraperProcess(current_app, flask_login.current_user.id, tag_name, work_id).start_process()

            flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

        else:
            flash(MessagesConsts.SCRAPING_PROCESS_FOR_WORK_ID_RUNNING.format(work_id=work_id), FlashConsts.DANGER)

        return redirect(url_for("works.add_work"))

    return render_template("add_work.html",
                           add_work_form=add_work_form,
                           running_processes=running_processes)


@works.route("/<work_id>/management/remove", methods=["POST"])
@flask_login.login_required
def remove_work(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        tag_name = user_work.tag.name
        db_utils.remove_object_from_db(user_work)

        flash(MessagesConsts.WORK_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=tag_name))

    else:
        abort(404)


@works.route("/<work_id>/download", methods=["GET"])
@flask_login.login_required
def download_work(work_id):
    user_work = models.Work.query.filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)
            files_utils.write_work_to_files(user_work, tmp_dir_path)

            archive_name = f"{user_work.name.replace(' ', '_')}.zip"
            archive_path = os.path.join(tmp_dir_path, archive_name)

            files_utils.zip_files(archive_path, tmp_dir_path, (".zip",))

            return send_file(archive_path, as_attachment=True, max_age=0, download_name=archive_name)

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
