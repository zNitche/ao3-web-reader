import tempfile
import zipfile
import os
from flask import Blueprint, render_template, flash, abort, redirect, \
    url_for, make_response, request, send_file
from ao3_web_reader.consts import FlashConsts, MessagesConsts, PaginationConsts
from ao3_web_reader import models, db, processes_manager, forms, auth_manager
from ao3_web_reader.authentication.decorators import login_required
from ao3_web_reader.db import Pagination
from ao3_web_reader.modules.tasks import ScraperTask, ChapterUpdaterTask, WorkUpdaterTask
from ao3_web_reader.ebook_exporter import HTMLExporter, EpubExporter
from ao3_web_reader.utils import works_utils


works = Blueprint("works", __name__, template_folder="templates",
                  static_folder="static", url_prefix="/works")


@works.route("/<tag_name>", defaults={"page_id": 1})
@works.route("/<tag_name>/<int:page_id>")
@login_required
def all_works(tag_name, page_id):
    user = auth_manager.current_user()
    tag = models.Tag.query.filter_by(owner_id=user.id, name=tag_name).first()

    if tag:
        search_string = request.args.get(
            "search") if request.args.get("search") is not None else ""

        only_favorites = request.args.get("only_favorites")
        only_favorites = int(
            only_favorites) if only_favorites is not None else 0

        works_query = models.Work.query.filter(models.Work.name.icontains(search_string),
                                               models.Work.tag_id == tag.id,
                                               models.Work.owner_id == user.id,
                                               models.Work.was_removed == False).\
            order_by(models.Work.last_updated.desc())

        if only_favorites:
            works_query = works_query.filter(models.Work.favorite == True)

        works_pagination = Pagination(
            query=works_query, page_id=page_id, items_per_page=PaginationConsts.WORKS_PER_PAGE)

        return render_template("works.html",
                               tag=tag,
                               works_pagination=works_pagination,
                               works=works_pagination.items,
                               only_favorites=only_favorites,
                               search_string=search_string)

    abort(404)


@works.route("/<tag_name>/removed-works", defaults={"page_id": 1})
@works.route("/<tag_name>/removed_works/<int:page_id>")
@login_required
def removed_works(tag_name, page_id):
    user = auth_manager.current_user()
    tag = models.Tag.query.filter_by(owner_id=user.id, name=tag_name).first()

    if tag:
        works_query = models.Work.query.filter_by(tag_id=tag.id, owner_id=user.id, was_removed=True).order_by(
            models.Work.last_updated.desc())

        works_pagination = Pagination(
            query=works_query, page_id=page_id, items_per_page=PaginationConsts.WORKS_PER_PAGE)

        return render_template("works.html",
                               tag=tag,
                               works_pagination=works_pagination,
                               works=works_pagination.items)

    abort(404)


@works.route("/add", methods=["GET", "POST"])
@login_required
def add_work():
    user = auth_manager.current_user()
    add_work_form = forms.AddWorkForm(user=user)

    tags = models.Tag.query.filter_by(owner_id=user.id).all()
    add_work_form.tag_name.choices = [tag.name for tag in tags]

    if add_work_form.validate_on_submit():
        work_id = add_work_form.work_id.data
        tag_name = add_work_form.tag_name.data

        running_processes = processes_manager.get_processes_data_for_user_and_work(
            "ScraperProcess", user.id, work_id)

        if len(running_processes) == 0:
            ScraperTask(user.id, tag_name, work_id).start_process()
            flash(MessagesConsts.SCRAPING_PROCESS_STARTED, FlashConsts.SUCCESS)

        else:
            flash(MessagesConsts.SCRAPING_PROCESS_FOR_WORK_ID_RUNNING.format(
                work_id=work_id), FlashConsts.DANGER)

        return redirect(url_for("works.add_work"))

    return render_template("add_work.html", add_work_form=add_work_form)


@works.route("/<work_id>/chapters/<chapter_id>/force-update", methods=["POST"])
@login_required
def force_chapter_update(work_id, chapter_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        work_chapter = models.Chapter.query.filter_by(
            work_id=user_work.id, chapter_id=chapter_id).first()

        running_processes = processes_manager.get_processes_data_for_user_and_chapter("ChapterUpdaterProcess",
                                                                                      user.id,
                                                                                      chapter_id)

        if len(running_processes) == 0:
            ChapterUpdaterTask(user.id, work_id, chapter_id).start_process()
            flash(MessagesConsts.CHAPTER_SCRAPING_PROCESS_STARTED,
                  FlashConsts.SUCCESS)

        if work_chapter:
            return redirect(url_for("works.chapter",
                                    work_id=work_id,
                                    chapter_id=chapter_id))

    abort(404)


@works.route("/<work_id>/force-chapters-update", methods=["GET"])
@login_required
def force_chapters_update(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        running_processes = processes_manager.get_processes_data_for_user_and_work("ChaptersUpdaterProcess",
                                                                                   user.id,
                                                                                   work_id)

        if len(running_processes) == 0:
            WorkUpdaterTask(user.id, work_id).start_process()
            flash(MessagesConsts.CHAPTERS_UPDATE_PROCESS_STARTED,
                  FlashConsts.SUCCESS)

        page_id = request.args.get("page_id")
        return redirect(url_for("works.all_works", tag_name=user_work.tag.name, page_id=page_id))

    abort(404)


@works.route("/<work_id>/management/remove", methods=["POST"])
@login_required
def remove_work(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        tag_name = user_work.tag.name
        db.remove(user_work)

        flash(MessagesConsts.WORK_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=tag_name))

    abort(404)


@works.route("/<work_id>/toggle-chapters-completion", methods=["POST"])
@login_required
def toggle_chapters_completion(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        for chapter in user_work.chapters:
            chapter.completed = not chapter.completed
            db.commit()

        page_id = request.args.get("page_id")

        flash(MessagesConsts.CHAPTERS_MARKED_AS_COMPLETED.format(
            work_name=user_work.name), FlashConsts.SUCCESS)
        return redirect(url_for("works.all_works", tag_name=user_work.tag.name, page_id=page_id))

    abort(404)


@works.route("/<work_id>/toggle-favorite", methods=["POST"])
@login_required
def toggle_work_favorite(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

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
@login_required
def download_work(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    export_target_type = request.args.get("type", None)

    if user_work:
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            match export_target_type:
                case "html":
                    exporter = HTMLExporter(user.id, user_work)
                    files_path = os.path.join(
                        tempfile.gettempdir(), tmp_dir_name)

                    exporter.export(files_path, prettify=True)
                    work_name = works_utils.serialize_work_name(user_work.name)

                    output_file_name = f"{work_name}.zip"
                    archive_path = os.path.join(
                        tempfile.gettempdir(), output_file_name)

                case "epub":
                    exporter = EpubExporter(user.id, user_work)
                    files_path = os.path.join(
                        tempfile.gettempdir(), tmp_dir_name)

                    exporter.export(files_path)
                    work_name = works_utils.serialize_work_name(user_work.name)

                    output_file_name = f"{work_name}.epub"
                    archive_path = os.path.join(
                        tempfile.gettempdir(), output_file_name)
    
                case _:
                    abort(400)

            abs_files_path = os.path.abspath(files_path)
            abs_files_name = os.path.relpath(files_path, os.path.dirname(abs_files_path))

            with zipfile.ZipFile(archive_path, mode="w") as archive:
                for (root, dirs, files) in os.walk(files_path):
                    root_abs = os.path.abspath(root)
                    abs_root_name = os.path.relpath(root, os.path.dirname(root_abs))

                    diff_root = bool(abs_files_name != abs_root_name)

                    if diff_root:
                        archive.write(root, arcname=abs_root_name)

                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(abs_root_name, file) if diff_root else file

                        archive.write(file_path, arcname=arcname)

            return send_file(archive_path, as_attachment=True, max_age=0, download_name=output_file_name)

    abort(404)


@works.route("/<work_id>/chapters")
@login_required
def chapters(work_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        available_chapters = user_work.get_not_removed_chapters()
        removed_chapters = user_work.get_removed_chapters()

        return render_template("chapters.html", work=user_work, available_chapters=available_chapters,
                               removed_chapters=removed_chapters)

    abort(404)


@works.route("/<work_id>/chapters/<chapter_id>")
@login_required
def chapter(work_id, chapter_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        work_chapter = models.Chapter.query.filter_by(
            work_id=user_work.id, chapter_id=chapter_id).first()

        if work_chapter:
            running_processes = processes_manager.get_processes_data_for_user_and_chapter("ChapterUpdaterProcess",
                                                                                          user.id,
                                                                                          chapter_id)
            return render_template("chapter.html",
                                   chapter=work_chapter,
                                   updating_chapter=True if len(running_processes) > 0 else False)

    abort(404)


@works.route("/<work_id>/chapters/<chapter_id>/toggle-completed-state", methods=["POST"])
@login_required
def chapter_toggle_completed_state(work_id, chapter_id):
    user = auth_manager.current_user()
    user_work = models.Work.query.filter_by(
        owner_id=user.id, work_id=work_id).first()

    if user_work:
        work_chapter = models.Chapter.query.filter_by(
            work_id=user_work.id, chapter_id=chapter_id).first()

        if work_chapter:
            work_chapter.completed = not work_chapter.completed
            db.commit()

            return make_response({
                "status": not work_chapter.completed
            }, 200)

    abort(404)
