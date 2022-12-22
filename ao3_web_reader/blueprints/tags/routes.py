from flask import Blueprint, render_template, flash, redirect, url_for, abort
import flask_login
from ao3_web_reader import models
from ao3_web_reader.consts import FlashConsts, MessagesConsts
from ao3_web_reader.app_modules import forms
from ao3_web_reader.utils import db_utils


tags = Blueprint("tags", __name__, template_folder="templates", static_folder="static", url_prefix="/tags")


@tags.route("/")
@flask_login.login_required
def all_tags():
    tags = models.Tag.query.filter_by(owner_id=flask_login.current_user.id).all()

    return render_template("tags.html", tags=tags)


@tags.route("/add_tag", methods=["GET", "POST"])
@flask_login.login_required
def add_tag():
    add_tag_form = forms.AddTagForm()

    if add_tag_form.validate_on_submit():
        tag = models.Tag(name=add_tag_form.tag_name.data, owner_id=flask_login.current_user.id)
        db_utils.add_object_to_db(tag)

        flash(MessagesConsts.ADDED_TAG.format(tag_name=tag.name), FlashConsts.SUCCESS)

        return redirect(url_for("tags.add_tag"))

    return render_template("add_tag.html", add_tag_form=add_tag_form)


@tags.route("/tags/<tag_name>/management")
@flask_login.login_required
def tag_management(tag_name):
    tag = models.Tag.query.filter_by(owner_id=flask_login.current_user.id, name=tag_name).first()

    if tag:
        return render_template("tag_management.html", tag=tag)

    abort(404)


@tags.route("/<tag_id>/management/remove", methods=["POST"])
@flask_login.login_required
def remove_tag(tag_id):
    user_tag = models.Tag.query.filter_by(owner_id=flask_login.current_user.id, id=tag_id).first()

    if user_tag:
        for work in user_tag.works:
            work_related_messages = models.UpdateMessage.query.filter_by(work_name=work.name).all()

            for message in work_related_messages:
                db_utils.remove_object_from_db(message)

        db_utils.remove_object_from_db(user_tag)

        flash(MessagesConsts.TAG_REMOVED, FlashConsts.SUCCESS)
        return redirect(url_for("tags.all_tags"))

    else:
        abort(404)
