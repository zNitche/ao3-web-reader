import tempfile
import os
from flask import Blueprint, render_template, flash, redirect, url_for, abort, send_file
import flask_login
from ao3_web_reader import models, db
from ao3_web_reader.consts import FlashConsts, MessagesConsts
from ao3_web_reader.app_modules import forms
from ao3_web_reader.utils import files_utils


tags = Blueprint("tags", __name__, template_folder="templates", static_folder="static", url_prefix="/tags")


@tags.route("/")
@flask_login.login_required
def all_tags():
    tags = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id).all()

    return render_template("tags.html", tags=tags)


@tags.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add_tag():
    add_tag_form = forms.AddTagForm()

    if add_tag_form.validate_on_submit():
        tag = models.Tag(name=add_tag_form.tag_name.data, owner_id=flask_login.current_user.id)
        db.add(tag)

        flash(MessagesConsts.ADDED_TAG.format(tag_name=tag.name), FlashConsts.SUCCESS)
        return redirect(url_for("tags.add_tag"))

    return render_template("add_tag.html", add_tag_form=add_tag_form)


@tags.route("/<tag_id>/management/remove", methods=["POST"])
@flask_login.login_required
def remove_tag(tag_id):
    user_tag = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id, id=tag_id).first()

    if user_tag:
        db.remove(user_tag)

        flash(MessagesConsts.TAG_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("tags.all_tags"))

    abort(404)


@tags.route("/<tag_id>/download", methods=["GET"])
@flask_login.login_required
def download_tag(tag_id):
    tag = db.session.query(models.Tag).filter_by(owner_id=flask_login.current_user.id, id=tag_id).first()

    if tag:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_dir_path = os.path.join(tempfile.gettempdir(), tmpdir)

            for work in tag.works:
                work_name = work.name.replace("/", "-")

                work_path = os.path.join(tmp_dir_path, work_name)

                os.mkdir(work_path)

                files_utils.write_work_to_files(work, work_path)

            archive_name = f"{tag.name}.zip"
            archive_path = os.path.join(tmp_dir_path, archive_name)

            files_utils.zip_files(archive_path, tmp_dir_path, (".zip",))

            return send_file(archive_path, as_attachment=True, max_age=0, download_name=archive_name)

    abort(404)
