from typing import TypeVar
from sqlalchemy import Select
from ao3_web_reader.db.model_base import ModelBase

T = TypeVar("T", bound="ModelBase")

class Pagination:
    def __init__(self, db_model: type[T], query: Select[T], page_id: int, items_per_page=25):
        self.__db_model = db_model
        self.__query = query

        self.total_items_count = self.__get_files_count()

        self.page_id = page_id
        self.items_per_page = items_per_page
        self.is_page_id_valid = self.__validate_page_id()

        self.has_next = False
        self.has_prev = page_id > 1
        self.prev_num = page_id - 1 if self.has_prev else 1
        self.next_num = page_id

        self.items = self.__query_items()

    def __get_files_count(self):
        count = self.__db_model.count(self.__query)
        return count if count is not None else 0

    def __get_offset(self):
        return (self.page_id - 1) * self.items_per_page if self.page_id > 0 else 0

    def __query_items(self):
        count = self.total_items_count if self.total_items_count is not None else 0

        offset = self.__get_offset()

        self.has_next = count > offset + self.items_per_page
        self.next_num = self.page_id + 1 if self.has_next else self.page_id

        query_exp = self.__query.limit(self.items_per_page).offset(offset)

        return self.__db_model.scalar(query_exp).unique().all()

    def __validate_page_id(self) -> bool:
        return True if self.__get_offset() <= self.total_items_count else False
