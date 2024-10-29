from flask import Blueprint, render_template, redirect, url_for, flash
import flask_login
from werkzeug.security import check_password_hash
from ao3_web_reader.app_modules import forms
from ao3_web_reader import models, db
from ao3_web_reader.consts import MessagesConsts, FlashConsts


auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static", url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("core.home"))

    login_form = forms.LoginForm()

    if login_form.validate_on_submit():
        user = db.session.query(models.User).filter_by(username=login_form.username.data).first()

        if user and check_password_hash(user.password, login_form.password.data):
            flask_login.login_user(user)

            return redirect(url_for("core.home"))

        else:
            flash(MessagesConsts.LOGIN_ERROR, FlashConsts.DANGER)

    return render_template("login.html", login_form=login_form)


@auth.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()

    return redirect(url_for("core.home"))
