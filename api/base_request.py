import pprint
import time

import requests

BASE_URL_PETSTORE = "https://petstore.swagger.io/v2"


class BaseRequest:
    def __init__(self, base_url=BASE_URL_PETSTORE, attempts=5, delay_seconds=1):
        self.base_url = base_url
        self.attempts = attempts
        self.delay_seconds = delay_seconds
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def _request(self, method, endpoint, body=None, params=None, expected_status=200):
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(1, self.attempts + 1):
            response = requests.request(
                method, url, json=body, params=params, headers=self.headers, timeout=15
            )
            self._log(method, response, attempt)

            if expected_status is None or response.status_code == expected_status:
                return response

            time.sleep(self.delay_seconds)

        return response

    def _log(self, method, response, attempt):
        pprint.pprint(f"{method} (попытка {attempt})")
        pprint.pprint(response.url)
        pprint.pprint(f"{response.status_code} {response.reason}")
        pprint.pprint(response.text)
        pprint.pprint("**********")

    def get(self, endpoint, params=None, expected_status=200):
        return self._request("GET", endpoint, params=params, expected_status=expected_status)

    def post(self, endpoint, body, expected_status=200):
        return self._request("POST", endpoint, body=body, expected_status=expected_status)

    def put(self, endpoint, body, expected_status=200):
        return self._request("PUT", endpoint, body=body, expected_status=expected_status)

    def delete(self, endpoint, expected_status=200):
        return self._request("DELETE", endpoint, expected_status=expected_status)
