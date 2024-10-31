from flask import url_for
from tests.consts import UsersConsts


def test_fail_login(test_client):
    from ao3_web_reader import forms

    form = forms.LoginForm()
    form.username.data = UsersConsts.TEST_USER_NAME
    form.password.data = "wrong_pass"

    response = test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_success_login(test_client):
    from ao3_web_reader import forms

    form = forms.LoginForm()
    form.username.data = UsersConsts.TEST_USER_NAME
    form.password.data = UsersConsts.TEST_USER_PASSWORD

    response = test_client.post(url_for("auth.login"), data=form.data, follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("core.home")


def test_logout(test_client, logged_test_user):
    response = test_client.get(url_for("auth.logout"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")

    response = test_client.get(url_for("core.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")
