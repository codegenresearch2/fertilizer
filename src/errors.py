import sys
from time import sleep, time
from math import exp
import json

import requests
from colorama import Fore

class AuthenticationError(Exception):
  pass

class TorrentDecodingError(Exception):
  pass

class UnknownTrackerError(Exception):
  pass

class TorrentNotFoundError(Exception):
  pass

class TorrentAlreadyExistsError(Exception):
  pass

class ConfigKeyError(Exception):
  pass

class TorrentClientError(Exception):
  pass

class TorrentInjectionError(Exception):
  pass

def handle_error(
  description: str,
  exception_details: (str | None) = None,
  wait_time: int = 0,
  extra_description: str = "",
  should_exit: bool = False,
) -> None:
  action = "Exiting" if should_exit else "Retrying"
  action += f" in {wait_time} seconds..." if wait_time else "..."
  exception_message = f"\n{Fore.LIGHTBLACK_EX}{exception_details}" if exception_details is not None else ""

  print(f"{Fore.RED}Error: {description}{extra_description}. {action}{exception_message}{Fore.RESET}")
  sleep(wait_time)

  if should_exit:
    sys.exit(1)

class GazelleAPI:
  def __init__(self, site_url, tracker_url, auth_header, rate_limit):
    self._s = requests.session()
    self._s.headers.update(auth_header)
    self._rate_limit = rate_limit
    self._timeout = 15
    self._last_used = 0

    self._max_retries = 20
    self._max_retry_time = 600
    self._retry_wait_time = lambda x: min(int(exp(x)), self._max_retry_time)

    self._announce_url = None
    self.sitename = self.__class__.__name__
    self.site_url = site_url
    self.tracker_url = tracker_url
    self.api_url = f"{self.site_url}/ajax.php"

  def _request_with_retry(self, action, **params):
    current_retries = 1

    while current_retries <= self._max_retries:
      now = time()
      if (now - self._last_used) > self._rate_limit:
        self._last_used = now
        params["action"] = action

        try:
          response = self._s.get(self.api_url, params=params, timeout=self._timeout)
          response.raise_for_status()  # raise exception if status is not 200
          return json.loads(response.text)
        except requests.exceptions.Timeout as e:
          error_code = "TimeoutError"
          description = "Request timed out"
        except requests.exceptions.ConnectionError as e:
          error_code = "ConnectionError"
          description = "Unable to connect"
        except requests.exceptions.HTTPError as e:
          error_code = "HTTPError"
          description = "HTTP request failed"
        except requests.exceptions.RequestException as e:
          error_code = "RequestError"
          description = f"Request failed: {type(e).__name__}: {e}"
        except json.JSONDecodeError as e:
          error_code = "JSONDecodingError"
          description = "JSON decoding of response failed"

        handle_error(
          description=description,
          exception_details=f"{error_code}: {e}",
          wait_time=self._retry_wait_time(current_retries),
          extra_description=f" (attempt {current_retries}/{self._max_retries})",
        )
        current_retries += 1
      else:
        sleep(0.2)

    handle_error(description="Maximum number of retries reached", should_exit=True)

  def get_account_info(self) -> dict:
    try:
      r = self._request_with_retry("index")
      if r["status"] != "success":
        raise AuthenticationError(r["error"])
      return r
    except AuthenticationError as e:
      handle_error(description=f"Authentication to {self.sitename} failed", exception_details=e, should_exit=True)

  def find_torrent(self, torrent_hash: str) -> dict:
    return self._request_with_retry("torrent", hash=torrent_hash)

  @property
  def announce_url(self) -> str:
    if self._announce_url is None:
      self._announce_url = self.__get_announce_url()
    return self._announce_url

  def __get_announce_url(self):
    try:
      account_info = self.get_account_info()
    except AuthenticationError as e:
      handle_error(description=f"Authentication to {self.sitename} failed", exception_details=e, should_exit=True)

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

This code includes the error handling improvements such as raising specific exceptions for different errors and handling authentication errors gracefully. It also encapsulates the request logic for reusability.