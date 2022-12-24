from flask import Blueprint, render_template, flash, abort, redirect, url_for, current_app, send_file
import flask_login
from ao3_web_reader.app_modules import forms
from ao3_web_reader.consts import FlashConsts, MessagesConsts
from ao3_web_reader.utils import db_utils
from ao3_web_reader import models
from ao3_web_reader.app_modules.processes.scraper_process import ScraperProcess
import tempfile
import zipfile
import os


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/<tag_name>")
@flask_login.login_required
def all_works(tag_name):
    tag = models.Tag.query.filter_by(owner_id=flask_login.current_user.id, name=tag_name).first()

    if tag:
        return render_template("works.html", works=tag.works)

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

        ScraperProcess(current_app, flask_login.current_user.id, tag_name, work_id).start_process()

        flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

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
            for chapter in user_work.chapters:
                tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)
                chapter_file_path = os.path.join(tmp_dir_path, f"{chapter.title}.txt")

                with open(chapter_file_path, "a") as chapter_file:
                    for row in chapter.rows:
                        chapter_file.write(row.content)
                        chapter_file.write("\n")

            archive_name = f"{user_work.name.replace(' ', '_')}.zip"
            archive_path = os.path.join(tmp_dir_path, archive_name)

            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for file in os.listdir(tmp_dir_path):
                    if file.endswith(".txt"):
                        file_path = os.path.join(tmp_dir_path, file)

                        archive.write(file_path, file)

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
