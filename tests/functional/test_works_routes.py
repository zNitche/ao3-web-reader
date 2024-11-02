from flask import url_for

from ao3_web_reader import models, db, auth_manager


def test_works_preview(test_client, logged_test_user):
    user = auth_manager.current_user()
    tag = models.Tag(name="test_tag", owner_id=user.id)
    db.session.add(tag)
    db.session.commit()

    response = test_client.get(url_for("works.all_works", tag_name=tag.name), follow_redirects=True)

    assert response.status_code == 200
    assert response.request.path == url_for("works.all_works", tag_name=tag.name)
