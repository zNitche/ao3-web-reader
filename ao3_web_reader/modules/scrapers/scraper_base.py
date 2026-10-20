import bs4
from dataclasses import dataclass
from datetime import datetime
from ao3_web_reader.modules.helpers import RequestsHandler


@dataclass
class ChapterStruct:
    work_id: str
    name: str
    id: str
    url: str
    date: datetime
    content: str | None
    order_id: int


@dataclass
class WorkStruct:
    name: str
    url: str
    id: str
    chapters: list[ChapterStruct]
    # content: str


class ScraperBase():
    def __init__(self, work_id: str) -> None:
        self.requests_handler = RequestsHandler()

        self.work_id = work_id
        self.work_soup: bs4.BeautifulSoup = self.get_work_soup() 

    def check_if_work_exists(self) -> bool:
        raise NotImplementedError()

    def get_chapters_structs(self) -> list[ChapterStruct]:
        raise NotImplementedError()

    def sanitize_html(self, soup: bs4.Tag) -> None:
        # https://validator.w3.org/feed/docs/warning/SecurityRisk.html
        dangerous_tags = ["comment", "embed", "link", "listing", "meta", "noscript", "object",
                          "plaintext", "script", "xmp", "img", "video", "audio", "iframe"]

        # Remove potentially dangerous tags
        for tag in dangerous_tags:
            target_tags = soup.find_all(tag, recursive=True)

            for target_tag in target_tags:
                target_tag.decompose()

        # Clear tags attributes
        for tag in soup.find_all(recursive=True):
            tag.attrs.clear()

    def sanitize_chapter_content(self, soup: bs4.Tag) -> None:
        raise NotImplementedError()

    def get_chapter_content(self, chapter_url: str) -> str:
        raise NotImplementedError()

    def get_chapter_data_struct(self, chapter: ChapterStruct):
        raise NotImplementedError()

    def get_work_soup(self) -> bs4.BeautifulSoup:
        raise NotImplementedError()

    def get_work_name(self) -> str:
        raise NotImplementedError()

    def get_work_description(self) -> str:
        raise NotImplementedError()

    def get_work_struct(self) -> WorkStruct:
        raise NotImplementedError()

    def get_work(self, progress_callback=None, delay_between_chapters=6) -> WorkStruct:
        raise NotImplementedError()

    def get_chapter_content_for_id(self, chapter_id: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def serialize_work_name(name: str) -> str:
        return name.replace("/", "-").replace(" ", "_").replace(".", "").replace("'s", "s")
