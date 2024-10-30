import pytest
from flask import url_for
from werkzeug.security import generate_password_hash
from ao3_web_reader import models, db
from ao3_web_reader import create_app
from tests.test_config import TestConfig
from tests.consts import UsersConsts


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app(TestConfig)
    client = flask_app.test_client()

    with flask_app.test_request_context():
        user = models.User(username=UsersConsts.TEST_USER_NAME,
                           password=UsersConsts.TEST_USER_PASSWORD)

        user.password = generate_password_hash(user.password)

        db.session.add(user)
        db.session.commit()

        yield client


@pytest.fixture(scope="function")
def logged_test_user(test_client):
    from ao3_web_reader.modules import forms

    form = forms.LoginForm()
    form.username.data = UsersConsts.TEST_USER_NAME
    form.password.data = UsersConsts.TEST_USER_PASSWORD

    test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    yield

    test_client.get(url_for("auth.logout"), follow_redirects=True)
