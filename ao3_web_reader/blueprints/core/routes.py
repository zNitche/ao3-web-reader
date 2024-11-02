from flask import Blueprint, render_template
from ao3_web_reader import models, auth_manager
from ao3_web_reader.authentication.decorators import login_required
from ao3_web_reader.db import Pagination
from ao3_web_reader.consts import PaginationConsts


core = Blueprint("core", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@core.route("/", defaults={"page_id": 1})
@core.route("/page/<int:page_id>")
@login_required
def home(page_id):
    user = auth_manager.current_user()
    user_works_ids = [work.id for work in user.works]

    messages_query = models.UpdateMessage.query.filter(models.UpdateMessage.work_id.in_(user_works_ids)).order_by(
        models.UpdateMessage.date.desc())

    messages_pagination = Pagination(query=messages_query,
                                     page_id=page_id,
                                     items_per_page=PaginationConsts.UPDATE_MESSAGES_PER_PAGE)

    return render_template("index.html",
                           messages_pagination=messages_pagination,
                           messages=messages_pagination.items)
