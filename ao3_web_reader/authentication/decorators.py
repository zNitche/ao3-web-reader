from functools import wraps
from flask import request, redirect, url_for, session, abort
from ao3_web_reader import auth_manager


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = session.get("auth_token")

        if not auth_token or not auth_manager.token_exists(auth_token):
            abort(401)

        current_user = auth_manager.user_for_token(auth_token)

        if not current_user:
            abort(401)

        request.__setattr__("current_user", current_user)

        auth_manager.refresh(auth_token)

        return f(*args, **kwargs)
    return decorated_function


def anonymous_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = session.get("auth_token")

        if auth_token and auth_manager.token_exists(auth_token):
            return redirect(url_for("core.home"))

        return f(*args, **kwargs)
    return decorated_function
