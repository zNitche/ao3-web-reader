import requests
from bs4 import BeautifulSoup
from ao3_web_reader.consts import AO3Consts
from ao3_web_reader.consts import WorksConsts


def check_if_work_exists(work_id):
    r = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id))

    return r.status_code == 200


def get_chapters_urls_data(soup):
    chapters_data = []

    chapters_nav = soup.find("ol", class_="chapter index group")

    if chapters_nav:
        chapters_nav_children = chapters_nav.findChildren("a", recursive=True)

        for item in chapters_nav_children:
            chapters_data.append({
                WorksConsts.NAME: item.text,
                WorksConsts.URL: item.attrs["href"]
                }
            )

    return chapters_data


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


def get_work_description(work_id):
    work_soup = get_work_soup(work_id)

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


def get_work(work_id):
    nav_soup = get_work_nav_soup(work_id)

    chapters_urls_data = get_chapters_urls_data(nav_soup)

    work_data = get_work_struct(work_id)

    for id, chapter_url_data in enumerate(chapters_urls_data):
        work_data[WorksConsts.CHAPTERS_DATA].append(get_chapter_data_from_url_data(id, chapter_url_data))

    return work_data


def get_chapter_data_from_url_data(chapter_id, url_data):
    chapter_data = {
            WorksConsts.ID: chapter_id,
            WorksConsts.NAME: url_data[WorksConsts.NAME],
            WorksConsts.CONTENT: get_work_content(url_data[WorksConsts.URL])
        }

    return chapter_data
