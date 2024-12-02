from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash
from ao3_web_reader import models, forms, auth_manager
from ao3_web_reader.consts import MessagesConsts, FlashConsts
from ao3_web_reader.authentication.decorators import login_required, anonymous_only


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
@anonymous_only
def login():
    login_form = forms.LoginForm()

    if login_form.validate_on_submit():
        user = models.User.query.filter_by(username=login_form.username.data).first()

        if user and check_password_hash(user.password, login_form.password.data):
            auth_manager.login(user.id)

            return redirect(url_for("core.home"))

        else:
            flash(MessagesConsts.LOGIN_ERROR, FlashConsts.DANGER)

    return render_template("login.html", login_form=login_form)


@auth.route("/logout")
@login_required
def logout():
    auth_manager.logout()

    return redirect(url_for("auth.login"))


@auth.route("/token", methods=["GET"])
@login_required
def user_auth_token():
    return auth_manager.get_auth_token_for_current_user()
