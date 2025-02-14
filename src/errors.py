import sys
from time import sleep
from math import exp
import json

import requests
from colorama import Fore

class RequestWrapper:
    def __init__(self, api_url, auth_header, rate_limit):
        self._s = requests.session()
        self._s.headers.update(auth_header)
        self._rate_limit = rate_limit
        self._timeout = 15
        self._last_used = 0
        self._max_retries = 20
        self._max_retry_time = 600
        self._retry_wait_time = lambda x: min(int(exp(x)), self._max_retry_time)
        self.api_url = api_url

    def get(self, action, **params):
        current_retries = 1
        while current_retries <= self._max_retries:
            now = time()
            if (now - self._last_used) > self._rate_limit:
                self._last_used = now
                params["action"] = action
                try:
                    response = self._s.get(self.api_url, params=params, timeout=self._timeout)
                    return json.loads(response.text)
                except requests.exceptions.Timeout:
                    error_code = 504
                except requests.exceptions.ConnectionError:
                    error_code = 503
                except requests.exceptions.RequestException:
                    error_code = 500
                except json.JSONDecodeError:
                    error_code = 400
                self._handle_error(error_code, current_retries)
                current_retries += 1
            else:
                sleep(0.2)
        self._handle_error(500, current_retries, should_exit=True)

    def _handle_error(self, error_code, current_retries, should_exit=False):
        error_messages = {
            504: "Request timed out",
            503: "Unable to connect",
            500: "Request failed",
            400: "JSON decoding of response failed",
        }
        description = error_messages.get(error_code, "Unknown error")
        action = "Exiting" if should_exit else "Retrying"
        wait_time = self._retry_wait_time(current_retries)
        extra_description = f" (attempt {current_retries}/{self._max_retries})"
        print(f"{Fore.RED}Error: {description}{extra_description}. {action} in {wait_time} seconds...{Fore.RESET}")
        sleep(wait_time)
        if should_exit:
            sys.exit(1)

class GazelleAPI:
    def __init__(self, site_url, tracker_url, auth_header, rate_limit):
        self._request = RequestWrapper(f"{site_url}/ajax.php", auth_header, rate_limit)
        self._announce_url = None
        self.sitename = self.__class__.__name__
        self.tracker_url = tracker_url

    def get_account_info(self):
        r = self._request.get("index")
        if r["status"] != "success":
            raise AuthenticationError(r["error"])
        return r

    def find_torrent(self, torrent_hash: str) -> dict:
        return self._request.get("torrent", hash=torrent_hash)

    @property
    def announce_url(self) -> str:
        if self._announce_url is None:
            self._announce_url = self.__get_announce_url()
        return self._announce_url

    def __get_announce_url(self):
        try:
            account_info = self.get_account_info()
        except AuthenticationError as e:
            print(f"{Fore.RED}Error: Authentication to {self.sitename} failed. Exiting...{Fore.RESET}")
            sys.exit(1)
        passkey = account_info["response"]["passkey"]
        return f"{self.tracker_url}/{passkey}/announce"

class OpsAPI(GazelleAPI):
    def __init__(self, api_key, delay_in_seconds=2):
        super().__init__(
            site_url="https://orpheus.network",
            tracker_url="https://home.opsfet.ch",
            auth_header={"Authorization": f"token {api_key}"},
            rate_limit=delay_in_seconds,
        )
        self.sitename = "OPS"

class RedAPI(GazelleAPI):
    def __init__(self, api_key, delay_in_seconds=2):
        super().__init__(
            site_url="https://redacted.ch",
            tracker_url="https://flacsfor.me",
            auth_header={"Authorization": api_key},
            rate_limit=delay_in_seconds,
        )
        self.sitename = "RED"


In the rewritten code, I have encapsulated the request logic in a `RequestWrapper` class for improved abstraction. I have also defined error codes for clarity and to avoid infinite loops in authentication. I have explicitly and clearly handled authentication errors.