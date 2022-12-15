import requests
from ao3_web_reader.consts import AO3Consts


def check_if_work_exists(work_id):
    r = requests.get(AO3Consts.AO3_WORKS_URL.format(work_id=work_id))

    return r.status_code == 200
