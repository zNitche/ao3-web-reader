from flask import url_for
from flask_login import current_user
from ao3_web_reader import models, db


def test_tags_preview(test_client, logged_test_user):
    response = test_client.get(url_for("tags.all_tags"), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("tags.all_tags")


def test_tags_management_preview(test_client, logged_test_user):
    tag = models.Tag(name="test_tag", owner_id=current_user.id)
    db.session.add(tag)
    db.session.commit()

    response = test_client.get(url_for("tags.tag_management", tag_name=tag.name), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("tags.tag_management", tag_name=tag.name)


def test_remove_tag(test_client, logged_test_user):
    tag = models.Tag(name="test_tag", owner_id=current_user.id)
    db.session.add(tag)
    db.session.commit()

    response = test_client.post(url_for("tags.remove_tag", tag_id=tag.id), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("tags.all_tags")



