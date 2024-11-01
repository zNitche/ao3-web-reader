import secrets
from ao3_web_reader.modules.managers import RedisClient
from ao3_web_reader import models


class AuthManager:
    def __init__(self, auth_db: RedisClient):
        self.__auth_db = auth_db

    def login(self, user_id: int):
        token = secrets.token_hex(128)
        self.__auth_db.set_value(token, user_id, ttl=600)

        return token

    def refresh(self, token: str):
        self.__auth_db.update_ttl(token, ttl=3600)

    def logout(self, token: int):
        self.__auth_db.delete_key(token)

    def token_exists(self, token: str):
        user_id = self.__auth_db.get_value(token)

        return True if user_id is not None else False

    def current_user(self, request):
        try:
            return request.current_user

        except:
            pass

        return None

    def user_for_token(self, token: str):
        user_id = self.__auth_db.get_value(token)

        if user_id is None:
            return None

        return models.User.query.filter_by(id=user_id).first()
