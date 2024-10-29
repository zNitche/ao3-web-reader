from flask import Blueprint, render_template
import flask_login
from ao3_web_reader import models, db
from ao3_web_reader.db import Pagination
from ao3_web_reader.consts import PaginationConsts


core = Blueprint("core", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@core.route("/", defaults={"page_id": 1})
@core.route("/page/<int:page_id>")
@flask_login.login_required
def home(page_id):
    user_works_ids = [work.id for work in flask_login.current_user.works]

    messages_query = db.session.query(models.UpdateMessage).filter(models.UpdateMessage.work_id.in_(user_works_ids)).order_by(
        models.UpdateMessage.date.desc())

    messages_pagination = Pagination(query=messages_query,
                                     page_id=page_id,
                                     items_per_page=PaginationConsts.UPDATE_MESSAGES_PER_PAGE)

    return render_template("index.html",
                           messages_pagination=messages_pagination,
                           messages=messages_pagination.items)
