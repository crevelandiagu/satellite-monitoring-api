import os
import requests
from abc import ABC


class HTTPClient(ABC):
    def __init__(self):
        self.read_timeout = os.getenv("READ_TIMEOUT_HTTPS", 10)
        self.connect_timeout = os.getenv("CONNECT_TIMEOUT_HTTPS", 10)

    def get(self, url, headers={}):
        return requests.get(
            url=url,
            headers=headers,
            timeout=(
                self.connect_timeout,
                self.read_timeout
            ),
            stream=True
        ).raw

    def post(self):
        pass