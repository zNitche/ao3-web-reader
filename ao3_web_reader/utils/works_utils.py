import requests
from bs4 import BeautifulSoup
from ao3_web_reader.consts import AO3Consts
from ao3_web_reader.consts import WorksConsts, ChaptersConsts
from datetime import datetime
import time


def check_if_work_exists(work_id):
    r = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id))

    return not r.status_code == 404


def check_if_work_is_accessible(work_id):
    r = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id))

    return r.status_code == 200


def get_chapters_struct(work_id):
    chapters_data = []

    html_nav_content = requests.get(AO3Consts.AO3_WORKS_NAVIGATION_URL.format(work_id=work_id)).text
    nav_soup = BeautifulSoup(html_nav_content, "html.parser")

    chapters_nav = nav_soup.find("ol", class_="chapter index group")

    if chapters_nav:
        chapters_nav_children = chapters_nav.findChildren("li", recursive=True)

        for id, item in enumerate(chapters_nav_children):
            chapter_href = item.findChild("a")
            chapter_date = item.findChild("span", class_="datetime").text.replace("(", "").replace(")", "")
            chapter_url = AO3Consts.AO3_URL + chapter_href.attrs["href"]

            chapters_data.append({
                ChaptersConsts.WORK_ID: work_id,
                ChaptersConsts.NAME: chapter_href.text,
                ChaptersConsts.ID: chapter_url.split("/")[-1],
                ChaptersConsts.URL: chapter_url,
                ChaptersConsts.DATE: datetime.strptime(chapter_date, "%Y-%m-%d"),
                ChaptersConsts.ORDER_ID: id
                }
            )

    return chapters_data


def get_chapter_content(chapter_url):
    content_data = []

    html_content = requests.get(chapter_url).text

    soup = BeautifulSoup(html_content, "html.parser")
    content_paragraphs = soup.find("div", class_="userstuff module").findChildren("p", recursive=True)

    for line in content_paragraphs:
        content_data.append(line.text)

    return content_data


def get_chapter_data_struct(chapter_struct):
    chapter_content = get_chapter_content(chapter_struct[ChaptersConsts.URL])
    chapter_struct[ChaptersConsts.CONTENT] = chapter_content

    return chapter_struct


def get_work_soup(work_id):
    html_work_content = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id)).text
    work_soup = BeautifulSoup(html_work_content, "html.parser")

    return work_soup


def get_work_name(work_id, work_soup=None):
    work_soup = get_work_soup(work_id) if work_soup is None else work_soup

    name_wrapper = work_soup.find("h2", class_="title heading")
    raw_name = name_wrapper.text

    name = raw_name.replace("\n", "").strip()

    return name


def get_work_description(work_id, work_soup=None):
    work_soup = get_work_soup(work_id) if work_soup is None else work_soup

    description_wrapper_container = work_soup.find("div", class_="summary module")
    description_wrapper = description_wrapper_container.find("blockquote", class_="userstuff")
    raw_description = description_wrapper.text

    return raw_description


def get_work_struct(work_id):
    struct = {
        WorksConsts.NAME: get_work_name(work_id),
        WorksConsts.WORK_ID: work_id,
        WorksConsts.CHAPTERS_DATA: []
    }

    return struct


def get_work(work_id, chapters_struct=None, progress_callback=None, delay_between_chapters=1):
    chapters_struct = chapters_struct if chapters_struct is not None else get_chapters_struct(work_id)
    work_data_struct = get_work_struct(work_id)

    for id, chapter_struct in enumerate(chapters_struct):
        work_data_struct[WorksConsts.CHAPTERS_DATA].append(get_chapter_data_struct(chapter_struct))

        if progress_callback is not None:
            progress_callback(id, len(chapters_struct))

        time.sleep(delay_between_chapters)

    return work_data_struct
