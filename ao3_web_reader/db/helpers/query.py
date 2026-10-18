from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar, Generic, Self, Any
from sqlalchemy import ScalarResult, Select, ColumnExpressionArgument

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
        self.__statement: Select[T] = self.__model.select()

    def __propagate(self, stm: Select[T]) -> Self:
        self.__statement = stm
        return self

    def order_by(self, *clauses: ColumnExpressionArgument[Any]) -> Self:
        return self.__propagate(self.__statement.order_by(*clauses))

    def filter(self, *criteria: ColumnExpressionArgument[bool]) -> Self:
        return self.__propagate(self.__statement.filter(*criteria))

    def filter_by(self, **kwargs) -> Self:
        return self.__propagate(self.__statement.filter_by(**kwargs))

    def limit(self, limit: int):
        return self.__propagate(self.__statement.limit(limit))

    def offset(self, offset: int):
        return self.__propagate(self.__statement.offset(offset))

    def count(self) -> int | None:
        return self.__model.count(self.__statement)

    def resolve(self) -> ScalarResult[T]:
        return self.__model.get_db_session().scalars(self.__statement)

    def first(self) -> T | None:
        return self.resolve().first()

    def all(self) -> Sequence[T]:
        return self.resolve().all()
