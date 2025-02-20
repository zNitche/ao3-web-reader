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

            chapter_nav_href = chapter_href.attrs["href"]

            chapter_id = chapter_nav_href.split("/")[-1]
            chapter_url = AO3Consts.AO3_CHAPTER_URL.format(chapter_id=chapter_id, work_id=work_id)

            chapters_data.append({
                ChaptersConsts.WORK_ID: work_id,
                ChaptersConsts.NAME: chapter_href.text,
                ChaptersConsts.ID: chapter_id,
                ChaptersConsts.URL: chapter_url,
                ChaptersConsts.DATE: datetime.strptime(chapter_date, "%Y-%m-%d"),
                ChaptersConsts.ORDER_ID: id
                }
            )

    return chapters_data


def sanitize_chapter_content(soup):
    # https://validator.w3.org/feed/docs/warning/SecurityRisk.html
    dangerous_tags = ["comment", "embed", "link", "listing", "meta", "noscript", "object",
                      "plaintext", "script", "xmp", "img", "video", "audio", "iframe"]

    # Clear landmarks
    for tag in soup.find_all("h3", class_="landmark", recursive=True):
        tag.decompose()

    # Remove potentially dangerous tags
    for tag in dangerous_tags:
        target_tags = soup.find_all(tag, recursive=True)

        for target_tag in target_tags:
            target_tag.decompose()

    # Clear tags attributes
    for tag in soup.find_all(recursive=True):
        tag.attrs.clear()


def get_chapter_content(chapter_url):
    html_content = requests.get(chapter_url).text

    soup = BeautifulSoup(html_content, "html.parser")

    chapter_content = soup.find("div", class_="userstuff module")

    if chapter_content is None:
        raise Exception("chapter content is empty")

    sanitize_chapter_content(chapter_content)
    parsed_content = "".join([str(tag) for tag in chapter_content.contents])

    return parsed_content


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

    header = work_soup.find("h4", class_="heading")
    name_wrapper = header.findChild("a")

    name = name_wrapper.text.replace("\n", "").strip()

    return name


def get_work_description(work_id, work_soup=None):
    work_soup = get_work_soup(work_id) if work_soup is None else work_soup

    description_wrapper = work_soup.find("blockquote", class_="userstuff")
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

def get_chapter(work_id, chapter_id):
    chapter_url = AO3Consts.AO3_CHAPTER_URL.format(chapter_id=chapter_id, work_id=work_id)
    chapter_content = get_chapter_content(chapter_url)

    return chapter_content

def serialize_work_name(name):
    return name.replace("/", "-").replace(" ", "_").replace(".", "").replace("'s", "s")
