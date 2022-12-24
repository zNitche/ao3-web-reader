from flask import url_for


def test_home_as_non_auth(test_client):
    response = test_client.get(url_for("main.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("auth.login")


def test_home_as_auth(test_client, logged_test_user):
    response = test_client.get(url_for("main.home"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("main.home")
