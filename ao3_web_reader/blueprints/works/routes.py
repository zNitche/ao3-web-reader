import tempfile
import os
from flask import Blueprint, render_template, flash, abort, redirect,\
    url_for, current_app, send_file, make_response, request
import flask_login
from ao3_web_reader.app_modules import forms
from ao3_web_reader.consts import FlashConsts, MessagesConsts, PaginationConsts
from ao3_web_reader.utils import files_utils
from ao3_web_reader import models, db
from ao3_web_reader.db import Pagination
from ao3_web_reader.app_modules.processes import ScraperProcess, ChapterUpdaterProcess


works = Blueprint("works", __name__, template_folder="templates", static_folder="static", url_prefix="/works")


@works.route("/<tag_name>", defaults={"page_id": 1})
@works.route("/<tag_name>/<int:page_id>")
@flask_login.login_required
def all_works(tag_name, page_id):
    user_id = flask_login.current_user.id
    tag = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id, name=tag_name).first()

    if tag:
        search_string = request.args.get("search") if request.args.get("search") is not None else ""
        only_favorites = int(request.args.get("only_favorites")) if request.args.get("only_favorites") is not None else 0

        works_query = db.session.query(models.Work).filter(models.Work.name.icontains(search_string),
                   models.Work.tag_id == tag.id,
                   models.Work.owner_id == user_id,
                   models.Work.was_removed == False).\
            order_by(models.Work.last_updated.desc())

        if only_favorites:
            works_query = works_query.filter(models.Work.favorite == True)

        works_pagination = Pagination(query=works_query, page_id=page_id, items_per_page=PaginationConsts.WORKS_PER_PAGE)

        return render_template("works.html",
                               tag=tag,
                               works_pagination=works_pagination,
                               works=works_pagination.items,
                               only_favorites=only_favorites,
                               search_string=search_string)

    abort(404)


@works.route("/<tag_name>/removed-works", defaults={"page_id": 1})
@works.route("/<tag_name>/removed_works/<int:page_id>")
@flask_login.login_required
def removed_works(tag_name, page_id):
    user_id = flask_login.current_user.id
    tag = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id, name=tag_name).first()

    if tag:
        works_query = db.session.query(models.Work).filter_by(tag_id=tag.id, owner_id=user_id, was_removed=True).order_by(
            models.Work.last_updated.desc())

        works_pagination = Pagination(query=works_query, page_id=page_id, items_per_page=PaginationConsts.WORKS_PER_PAGE)

        return render_template("works.html",
                               tag=tag,
                               works_pagination=works_pagination,
                               works=works_pagination.items)

    abort(404)


@works.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_work():
    add_work_form = forms.AddWorkForm()

    tags = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id).all()
    add_work_form.tag_name.choices = [tag.name for tag in tags]

    if add_work_form.validate_on_submit():
        work_id = add_work_form.work_id.data
        tag_name = add_work_form.tag_name.data

        running_processes = \
            current_app.processes_manager.get_processes_data_for_user_and_work("ScraperProcess",
                                                                               flask_login.current_user.id,
                                                                               work_id)

        if len(running_processes) == 0:
            ScraperProcess(current_app, flask_login.current_user.id, tag_name, work_id).start_process()
            flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

        else:
            flash(MessagesConsts.SCRAPING_PROCESS_FOR_WORK_ID_RUNNING.format(work_id=work_id), FlashConsts.DANGER)

        return redirect(url_for("works.add_work"))

    return render_template("add_work.html", add_work_form=add_work_form)


@works.route("/<work_id>/chapters/<chapter_id>/force-update", methods=["POST"])
@flask_login.login_required
def force_chapter_update(work_id, chapter_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        work_chapter = db.session.query(models.Chapter).filter_by(work_id=user_work.id, chapter_id=chapter_id).first()

        running_processes = \
            current_app.processes_manager.get_processes_data_for_user_and_chapter("ChapterUpdaterProcess",
                                                                               flask_login.current_user.id,
                                                                               chapter_id)

        if len(running_processes) == 0:
            ChapterUpdaterProcess(current_app, flask_login.current_user.id, work_id, chapter_id).start_process()
            flash(MessagesConsts.CHAPTER_SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

        if work_chapter:
            return redirect(url_for("works.chapter",
                                    work_id=work_id,
                                    chapter_id=chapter_id))

    abort(404)


@works.route("/<work_id>/management/remove", methods=["POST"])
@flask_login.login_required
def remove_work(work_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        tag_name = user_work.tag.name
        db.remove(user_work)

        flash(MessagesConsts.WORK_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=tag_name))

    abort(404)


@works.route("/<work_id>/toggle-chapters-completion", methods=["POST"])
@flask_login.login_required
def toggle_chapters_completion(work_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        for chapter in user_work.chapters:
            chapter.completed = not chapter.completed
            db.commit()

        page_id = request.args.get("page_id")

        flash(MessagesConsts.CHAPTERS_MARKED_AS_COMPLETED.format(work_name=user_work.name), FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=user_work.tag.name, page_id=page_id))

    abort(404)


@works.route("/<work_id>/toggle-favorite", methods=["POST"])
@flask_login.login_required
def toggle_work_favorite(work_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        user_work.favorite = not user_work.favorite
        db.commit()

        page_id = request.args.get("page_id")

        update_message = MessagesConsts.WORK_ADDED_TO_FAVORITES if user_work.favorite \
            else MessagesConsts.WORK_REMOVED_FROM_FAVORITES

        flash(update_message.format(work_name=user_work.name), FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=user_work.tag.name, page_id=page_id))

    abort(404)


@works.route("/<work_id>/download", methods=["GET"])
@flask_login.login_required
def download_work(work_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)
            files_utils.write_work_to_files(user_work, tmp_dir_path)

            archive_name = f"{user_work.name.replace(' ', '_')}.zip"
            archive_path = os.path.join(tmp_dir_path, archive_name)

            files_utils.zip_files(archive_path, tmp_dir_path, (".zip",))

            return send_file(archive_path, as_attachment=True, max_age=0, download_name=archive_name)

    abort(404)


@works.route("/<work_id>/chapters")
@flask_login.login_required
def chapters(work_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        available_chapters = user_work.get_not_removed_chapters()
        removed_chapters = user_work.get_removed_chapters()

        return render_template("chapters.html", work=user_work, available_chapters=available_chapters,
                               removed_chapters=removed_chapters)

    abort(404)


@works.route("/<work_id>/chapters/<chapter_id>")
@flask_login.login_required
def chapter(work_id, chapter_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        work_chapter = db.session.query(models.Chapter).filter_by(work_id=user_work.id, chapter_id=chapter_id).first()

        if work_chapter:
            running_processes = \
                current_app.processes_manager.get_processes_data_for_user_and_chapter("ChapterUpdaterProcess",
                                                                                      flask_login.current_user.id,
                                                                                      chapter_id)
            return render_template("chapter.html",
                                   chapter=work_chapter,
                                   updating_chapter=True if len(running_processes) > 0 else False)

    abort(404)


@works.route("/<work_id>/chapters/<chapter_id>/toggle-completed-state", methods=["POST"])
@flask_login.login_required
def chapter_toggle_completed_state(work_id, chapter_id):
    user_work = db.session.query(models.Work).filter_by(owner_id=flask_login.current_user.id, work_id=work_id).first()

    if user_work:
        work_chapter = db.session.query(models.Chapter).filter_by(work_id=user_work.id, chapter_id=chapter_id).first()

        if work_chapter:
            work_chapter.completed = not work_chapter.completed
            db.commit()

            return make_response({
                "status": not work_chapter.completed
            }, 200)

    abort(404)
