from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic
from sqlalchemy import ScalarResult, Sequence

# additional for pylance I guess...
if TYPE_CHECKING:
    from ao3_web_reader.db import ModelBase

# some syntax sugar for avoiding calling
# next_chapter = Chapter.query(Chapter.select().filter_by(work_id=self.work_id)).first()
# instead we can
# next_chapter = Chapter.query().filter_by(work_id=self.work_id).first()

T = TypeVar("T", bound="ModelBase")

class Query(Generic[T]):
    def __init__(self, cls: type[T]) -> None:
        self.__model: type[T] = cls

    def filter_by(self, **kwargs) -> ScalarResult[T]:
        return self.__model.get_db_session().scalars(self.__model.select().filter_by(**kwargs))

    def all(self) -> Sequence[T]:
        select = self.__model.select()
        return self.__model.get_db_session().scalars(select).all()  # type: ignore

    def first(self) -> T | None:
        select = self.__model.select()
        return self.__model.get_db_session().scalars(select).first()
