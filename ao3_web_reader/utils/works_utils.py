import requests
from bs4 import BeautifulSoup
from ao3_web_reader.consts import AO3Consts
from ao3_web_reader import models


def check_if_work_exists(work_id):
    r = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id))

    return r.status_code == 200


def get_works_urls_data(soup):
    works_data = []

    chapters_nav = soup.find("ol", class_="chapter index group")
    chapters_nav_children = chapters_nav.findChildren("a", recursive=True)

    for item in chapters_nav_children:
        works_data.append({
            "name": item.text,
            "url": item.attrs["href"]
            }
        )

    return works_data


def get_work_content(work_url):
    content_data = []

    url = AO3Consts.AO3_URL + work_url
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "html.parser")

    content = soup.find("div", class_="userstuff module")
    content_paragraphs = content.findChildren("p", recursive=True)

    for line in content_paragraphs:
        content_data.append(line.text)

    return content_data


def get_work_soup(work_id):
    html_work_content = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id)).text
    work_soup = BeautifulSoup(html_work_content, "html.parser")

    return work_soup


def get_work_nav_soup(work_id):
    html_nav_content = requests.get(AO3Consts.AO3_WORKS_NAVIGATION_URL.format(work_id=work_id)).text
    nav_soup = BeautifulSoup(html_nav_content, "html.parser")

    return nav_soup


def get_work_name(work_id):
    work_soup = get_work_soup(work_id)

    name_wrapper = work_soup.find("h2", class_="title heading")
    raw_name = name_wrapper.text

    name = raw_name.replace("\n", "").strip()

    return name


def get_work(work_id):
    nav_soup = get_work_nav_soup(work_id)

    works_urls_data = get_works_urls_data(nav_soup)

    work_data = {
        "name": get_work_name(work_id),
        "work_id": work_id,
        "chapters_data": []
    }

    for id, work_url_data in enumerate(works_urls_data):
        work_data["chapters_data"].append({
            "id": id,
            "name": work_url_data['name'],
            "content": get_work_content(work_url_data["url"])
        })

    return work_data


def create_chapters_models(work_data):
    chapters = []

    for chapter_data in work_data["chapters_data"]:
        chapter_id = chapter_data["id"]
        title = chapter_data["name"]
        content = chapter_data["content"]

        chapter = models.Chapter(title=title, chapter_id=chapter_id)

        for text in content:
            text_row = models.TextRow(content=text)
            chapter.rows.append(text_row)

        chapters.append(chapter)

    return chapters


def create_chapter_model(chapter_data):
    chapter_id = chapter_data["id"]
    title = chapter_data["name"]
    content = chapter_data["content"]

    chapter = models.Chapter(title=title, chapter_id=chapter_id)

    for text in content:
        text_row = models.TextRow(content=text)
        chapter.rows.append(text_row)

    return chapter


def create_work_model(work_data, owner_id):
    work = models.Work(name=work_data["name"], owner_id=owner_id, work_id=work_data["work_id"])

    return work
