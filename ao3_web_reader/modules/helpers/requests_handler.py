import requests
import time
from dataclasses import dataclass


DEFAULT_REQUESTS_USER_AGENT = "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
REQUEST_RECOVERABLE_STATUS_CODES = [495, 496, 502, 525, 526, 503]


@dataclass
class RequestsHandlerConfig:
    user_agent: str
    request_retries: int
    delay_between_tries: int


class RequestsHandler():
    def __init__(self) -> None:
        self.__config: RequestsHandlerConfig = self.__get_config()
        self.__req_session = self.__create_session()

    def __get_config(self) -> RequestsHandlerConfig:
        return RequestsHandlerConfig(user_agent=DEFAULT_REQUESTS_USER_AGENT,
                                     delay_between_tries=3, request_retries=5)

    def __create_session(self) -> requests.Session:
        s = requests.Session()
        s.headers.update(
            {"User-Agent": self.__config.user_agent if self.__config.user_agent else ""})

        return s

    def get(self, url: str, timeout: int = 15) -> requests.Response:
        retires_count = self.__config.request_retries

        for attempt in range(retires_count):
            response = self.__req_session.get(url, timeout=timeout)

            if response.ok:
                return response

            if response.status_code not in REQUEST_RECOVERABLE_STATUS_CODES:
                response.raise_for_status()

            if attempt < retires_count - 1:
                time.sleep(self.__config.delay_between_tries ** attempt)

        raise Exception(f"faield to fetch {url}")
