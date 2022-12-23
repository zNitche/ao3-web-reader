from flask import Blueprint, render_template
import flask_login
from ao3_web_reader import models
from ao3_web_reader.consts import PaginationConsts


main = Blueprint("main", __name__, template_folder="templates", static_folder="static", url_prefix="/")


@main.route("/", defaults={"page_id": 1})
@main.route("/page/<int:page_id>")
@flask_login.login_required
def home(page_id):
    user_works_ids = [work.id for work in flask_login.current_user.works]

    messages_query = models.UpdateMessage.query.filter(models.UpdateMessage.work_id.in_(user_works_ids)).order_by(
        models.UpdateMessage.date.desc())

    messages_pagination = messages_query.paginate(page=page_id, per_page=PaginationConsts.UPDATE_MESSAGES_PER_PAGE)

    return render_template("index.html",
                           messages_pagination=messages_pagination,
                           messages=messages_pagination.items)
