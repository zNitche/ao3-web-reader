import bs4
from datetime import datetime
import time
from ao3_web_reader.modules.scrapers import ScraperBase, ChapterStruct, WorkStruct


class AO3Consts:
    AO3_URL = "https://archiveofourown.org"
    AO3_WORKS_URL = AO3_URL + "/works/{work_id}"
    AO3_WORKS_NAVIGATION_URL = AO3_URL + "/works/{work_id}/navigate"
    AO3_CHAPTER_URL = AO3_WORKS_URL + "/chapters/{chapter_id}?view_adult=true"


class Ao3Scraper(ScraperBase):
    def __init__(self, work_id: str) -> None:
        super().__init__(work_id=work_id)

    def check_if_work_exists(self) -> bool:
        try:
            r = self.requests_handler.get(
                AO3Consts.AO3_WORKS_URL.format(work_id=self.work_id))

            return r.status_code == 200
        except Exception as e:
            pass

        return False

    def __get_nav_soup(self) -> bs4.BeautifulSoup | None:
        try:
            html_nav_content = self.requests_handler.get(
                AO3Consts.AO3_WORKS_NAVIGATION_URL.format(work_id=self.work_id)).text
            return bs4.BeautifulSoup(html_nav_content, "html.parser")

        except Exception as e:
            pass

        return None

    def get_chapters_structs(self) -> list[ChapterStruct]:
        chapters: list[ChapterStruct] = []

        nav_soup = self.__get_nav_soup()

        if not nav_soup:
            raise Exception("can't get navigation data")

        chapters_nav = nav_soup.find("ol", class_="chapter index group")

        if chapters_nav:
            chapters_nav_children = chapters_nav.find_all("li", recursive=True)

            for id, item in enumerate(chapters_nav_children):
                chapter_href = item.find("a")
                chapter_date = item.find("span", class_="datetime")

                if not chapter_href or not chapter_date:
                    raise Exception(
                        "error while getting chapters struct, chapter_href or chapter_date is None")

                chapter_date = chapter_date.text.replace(
                    "(", "").replace(")", "")
                chapter_nav_href: str = chapter_href.attrs["href"]

                chapter_id = chapter_nav_href.split("/")[-1]
                chapter_url = AO3Consts.AO3_CHAPTER_URL.format(
                    chapter_id=chapter_id, work_id=self.work_id)

                chapters.append(ChapterStruct(
                    work_id=self.work_id,
                    name=chapter_href.text,
                    id=chapter_id,
                    url=chapter_url,
                    date=datetime.strptime(chapter_date, "%Y-%m-%d"),
                    order_id=id,
                    content=None
                ))

        return chapters

    def sanitize_chapter_content(self, soup: bs4.Tag) -> None:
        for tag in soup.find_all(class_="landmark", recursive=True):
            tag.decompose()

        self.sanitize_html(soup=soup)

    def get_chapter_content_for_id(self, chapter_id: str) -> str:
        chapter_url = AO3Consts.AO3_CHAPTER_URL.format(
            chapter_id=chapter_id, work_id=self.work_id)

        return self.get_chapter_content(chapter_url=chapter_url)

    def get_chapter_content(self, chapter_url: str) -> str:
        try:
            html_content = self.requests_handler.get(chapter_url).text
        except Exception as e:
            raise Exception("can't get html content of chapter")

        soup = bs4.BeautifulSoup(html_content, "html.parser")
        chapter_content = soup.find("div", class_="userstuff module")

        if chapter_content is None:
            raise Exception("chapter content is empty")

        self.sanitize_chapter_content(chapter_content)
        parsed_content = "".join([str(tag)
                                  for tag in chapter_content.contents])

        return parsed_content

    def get_chapter_data_struct(self, chapter: ChapterStruct):
        chapter_content = self.get_chapter_content(chapter.url)
        chapter.content = chapter_content

    def get_work_soup(self) -> bs4.BeautifulSoup:
        try:
            html_content = self.requests_handler.get(
                url=AO3Consts.AO3_WORKS_URL.format(work_id=self.work_id)).text
        except Exception as e:
            raise Exception("can't get html content of work")

        return bs4.BeautifulSoup(html_content, "html.parser")

    def get_work_name(self) -> str:
        header = self.work_soup.find("h2", class_="heading")

        if not header:
            raise Exception("error while getting work name, header is None")

        work_name = header.text

        if not work_name:
            raise Exception(
                "error while getting work name, name_wrapper is None")

        return work_name.replace("\n", "").strip()

    def get_work_description(self) -> str:
        description_wrapper = self.work_soup.find(
            "blockquote", class_="userstuff")

        if not description_wrapper:
            raise Exception(
                "error while getting work description, description_wrapper is None")

        return description_wrapper.text

    def get_work_struct(self) -> WorkStruct:
        return WorkStruct(
            name=self.get_work_name(),
            id=self.work_id,
            chapters=[],
            url=AO3Consts.AO3_WORKS_URL.format(work_id=self.work_id),
        )

    def get_work(self, progress_callback=None, delay_between_chapters=6) -> WorkStruct:
        work_struct = self.get_work_struct()
        chapters_struct = self.get_chapters_structs()

        for id, chapter in enumerate(chapters_struct):
            chapter.content = self.get_chapter_content(chapter.url)
            work_struct.chapters.append(chapter)

            if progress_callback is not None:
                progress_callback(id, len(chapters_struct))

            time.sleep(delay_between_chapters)

        return work_struct
