class Pagination:
    def __init__(self, query, page_id, items_per_page=25):
        self.__query = query

        self.page_id = page_id
        self.items_per_page = items_per_page

        self.has_next = False
        self.has_prev = page_id > 1
        self.prev_num = page_id - 1 if self.has_prev else 1
        self.next_num = page_id

        self.items = self.__query_items()

    def __query_items(self):
        total_items = self.__query.count()
        offset = (self.page_id - 1) * self.items_per_page if self.page_id > 0 else 0

        self.has_next = total_items > offset + self.items_per_page
        self.next_num = self.page_id + 1 if self.has_next else self.page_id

        return self.__query.limit(self.items_per_page).offset(offset).all()
