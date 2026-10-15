from typing import Self
from sqlalchemy import Select, func, select, ScalarResult, MetaData
from sqlalchemy.orm import scoped_session, DeclarativeBase, Session
from ao3_web_reader.db.helpers import Query


class Base(DeclarativeBase):
    # https://alembic.sqlalchemy.org/en/latest/naming.html
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    @classmethod
    def get_db_session(cls) -> scoped_session[Session]:
        return None  # type: ignore

    @classmethod
    def select(cls) -> Select[Self]:
        return select(cls)

    @classmethod
    def query(cls: type[Self]) -> Query[Self]:
        return Query(cls)

    @classmethod
    def scalar(cls, select_exp: Select) -> ScalarResult[Self]:
        return cls.get_db_session().scalars(select_exp)

    @classmethod
    def count(cls, select_exp: Select) -> int | None:
        count = cls.get_db_session().scalar(
            select(func.count()).select_from(select_exp.subquery()))

        return count
