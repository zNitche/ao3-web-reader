from ao3_web_reader import db
from contextlib import contextmanager


def commit_session():
    try:
        db.session.commit()

    except:
        db.session.rollback()

        raise


def add_object_to_db(object):
    db.session.add(object)

    commit_session()


def remove_object_from_db(object):
    db.session.delete(object)

    commit_session()


@contextmanager
def db_session_scope(session=db.session):
    try:
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()
