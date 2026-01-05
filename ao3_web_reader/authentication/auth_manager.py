import secrets
from flask import g, session
from ao3_web_reader.modules.managers import CacheDatabase
from ao3_web_reader import models


class AuthManager:
    def __init__(self, auth_db: CacheDatabase):
        self.__auth_db = auth_db

    def login(self, user_id: int):
        token = secrets.token_hex(128)
        self.__auth_db.set_value(token, user_id, ttl=600)

        session["auth_token"] = token

    def refresh(self, token: str):
        self.__auth_db.update_ttl(token, ttl=3600)

    def logout(self):
        token = session.get("auth_token")
        self.__auth_db.delete_key(token)

        session.pop("auth_token")

    def token_exists(self, token: str):
        user_id = self.__auth_db.get_value(token)

        return True if user_id is not None else False

    def current_user(self) -> models.User:
        return g.get("current_user", None)

    def user_for_token(self, token: str):
        user_id = self.__auth_db.get_value(token)

        if user_id is None:
            return None

        return models.User.query.filter_by(id=user_id).first()

    def get_auth_token_for_current_user(self):
        return session.get("auth_token")
