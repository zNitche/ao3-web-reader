from __future__ import annotations

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

    def __return_self(self, stm: Select[T]) -> Self:
        self.__statement = stm
        return self

    def resolve(self) -> ScalarResult[T]:
        return self.__model.get_db_session().scalars(self.__statement)

    def order_by(self, *clauses: ColumnExpressionArgument[Any]) -> Self:
        return self.__return_self(self.__statement.order_by(*clauses))

    def filter(self, *criteria: ColumnExpressionArgument[bool]) -> Self:
        return self.__return_self(self.__statement.filter(*criteria))

    def filter_by(self, **kwargs) -> Self:
        return self.__return_self(self.__statement.filter_by(**kwargs))

    def limit(self, limit: int):
        return self.__return_self(self.__statement.limit(limit))

    def offset(self, offset: int):
        return self.__return_self(self.__statement.offset(offset))

    def count(self) -> int | None:
        return self.__model.count(self.__statement)
