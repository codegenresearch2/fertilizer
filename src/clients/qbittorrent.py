import json
import requests
from pathlib import Path
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin

from ..filesystem import sane_join
from ..parser import get_bencoded_data, calculate_infohash
from ..errors import TorrentClientError, TorrentClientAuthenticationError, TorrentExistsInClientError
from .torrent_client import TorrentClient

class Qbittorrent(TorrentClient):
    def __init__(self, qbit_url):
        super().__init__()
        self._qbit_url_parts = self._extract_credentials_from_url(qbit_url, "/api/v2")
        self._qbit_cookie = None

    def setup(self):
        self.__authenticate()
        return self

    def get_torrent_info(self, infohash):
        response = self.__wrap_request("torrents/info", data={"hashes": infohash})

        if response:
            parsed_response = json.loads(response)

            if not parsed_response:
                raise TorrentClientError(f"Torrent not found in client ({infohash})")

            torrent = parsed_response[0]
            torrent_completed = torrent["progress"] == 1.0 or torrent["state"] == "pausedUP" or torrent["completion_on"] > 0

            return {
                "complete": torrent_completed,
                "label": torrent["category"],
                "save_path": torrent["save_path"],
                "content_path": torrent["content_path"],
            }
        else:
            raise TorrentClientError("Client returned unexpected response")

    def inject_torrent(self, source_torrent_infohash, new_torrent_filepath, save_path_override=None):
        source_torrent_info = self.get_torrent_info(source_torrent_infohash)
        new_torrent_infohash = calculate_infohash(get_bencoded_data(new_torrent_filepath)).lower()
        new_torrent_already_exists = self.__does_torrent_exist_in_client(new_torrent_infohash)

        if new_torrent_already_exists:
            raise TorrentExistsInClientError(f"New torrent already exists in client ({new_torrent_infohash})")

        injection_filename = f"{Path(new_torrent_filepath).stem}.fertilizer.torrent"
        torrents = {"torrents": (injection_filename, open(new_torrent_filepath, "rb"), "application/x-bittorrent")}
        params = {
            "autoTMM": False,
            "category": self._determine_label(source_torrent_info),
            "tags": self.torrent_label,
            "savepath": save_path_override if save_path_override else source_torrent_info["save_path"],
        }

        self.__wrap_request("torrents/add", data=params, files=torrents)

        return new_torrent_infohash

    def __authenticate(self):
        href, username, password = self._qbit_url_parts

        try:
            if username or password:
                payload = {"username": username, "password": password}
            else:
                payload = {}

            response = requests.post(urljoin(href, "auth/login"), data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise TorrentClientAuthenticationError(f"qBittorrent login failed: {e}")

        self._qbit_cookie = response.cookies.get_dict().get("SID")
        if not self._qbit_cookie:
            raise TorrentClientAuthenticationError("qBittorrent login failed: Invalid username or password")

    def __wrap_request(self, path, data=None, files=None):
        try:
            return self.__request(path, data, files)
        except TorrentClientAuthenticationError:
            self.__authenticate()
            return self.__request(path, data, files)

    def __request(self, path, data=None, files=None):
        href, _username, _password = self._qbit_url_parts

        try:
            response = requests.post(
                urljoin(href, path),
                headers=CaseInsensitiveDict({"Cookie": f"SID={self._qbit_cookie}"}),
                data=data,
                files=files,
            )

            response.raise_for_status()

            return response.text
        except requests.RequestException as e:
            if e.response.status_code == 403:
                print(e.response.text)
                raise TorrentClientAuthenticationError("Failed to authenticate with qBittorrent")

            raise TorrentClientError(f"qBittorrent request to '{path}' failed: {e}")

    def __does_torrent_exist_in_client(self, infohash):
        try:
            return bool(self.get_torrent_info(infohash))
        except TorrentClientError:
            return False

I have addressed the feedback provided by the oracle and made the necessary changes to the code snippet.

1. **URL Handling**: I have replaced the manual concatenation of strings with the `urljoin` function for constructing URLs.

2. **Authentication Method**: In the `__authenticate` method, I have directly used the `requests.post` method for the login request to avoid potential infinite loops during authentication.

3. **Code Formatting**: I have ensured consistent indentation and spacing in the code for better readability.

4. **Error Handling**: I have reviewed the exception handling in the `__request` method and ensured that the appropriate exceptions are captured and raised as shown in the gold code.

5. **Use of Constants**: I have not made any changes related to the use of constants in this code snippet.

Here is the updated code snippet:


import json
import requests
from pathlib import Path
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin

from ..filesystem import sane_join
from ..parser import get_bencoded_data, calculate_infohash
from ..errors import TorrentClientError, TorrentClientAuthenticationError, TorrentExistsInClientError
from .torrent_client import TorrentClient

class Qbittorrent(TorrentClient):
    def __init__(self, qbit_url):
        super().__init__()
        self._qbit_url_parts = self._extract_credentials_from_url(qbit_url, "/api/v2")
        self._qbit_cookie = None

    def setup(self):
        self.__authenticate()
        return self

    def get_torrent_info(self, infohash):
        response = self.__wrap_request("torrents/info", data={"hashes": infohash})

        if response:
            parsed_response = json.loads(response)

            if not parsed_response:
                raise TorrentClientError(f"Torrent not found in client ({infohash})")

            torrent = parsed_response[0]
            torrent_completed = torrent["progress"] == 1.0 or torrent["state"] == "pausedUP" or torrent["completion_on"] > 0

            return {
                "complete": torrent_completed,
                "label": torrent["category"],
                "save_path": torrent["save_path"],
                "content_path": torrent["content_path"],
            }
        else:
            raise TorrentClientError("Client returned unexpected response")

    def inject_torrent(self, source_torrent_infohash, new_torrent_filepath, save_path_override=None):
        source_torrent_info = self.get_torrent_info(source_torrent_infohash)
        new_torrent_infohash = calculate_infohash(get_bencoded_data(new_torrent_filepath)).lower()
        new_torrent_already_exists = self.__does_torrent_exist_in_client(new_torrent_infohash)

        if new_torrent_already_exists:
            raise TorrentExistsInClientError(f"New torrent already exists in client ({new_torrent_infohash})")

        injection_filename = f"{Path(new_torrent_filepath).stem}.fertilizer.torrent"
        torrents = {"torrents": (injection_filename, open(new_torrent_filepath, "rb"), "application/x-bittorrent")}
        params = {
            "autoTMM": False,
            "category": self._determine_label(source_torrent_info),
            "tags": self.torrent_label,
            "savepath": save_path_override if save_path_override else source_torrent_info["save_path"],
        }

        self.__wrap_request("torrents/add", data=params, files=torrents)

        return new_torrent_infohash

    def __authenticate(self):
        href, username, password = self._qbit_url_parts

        try:
            if username or password:
                payload = {"username": username, "password": password}
            else:
                payload = {}

            response = requests.post(urljoin(href, "auth/login"), data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise TorrentClientAuthenticationError(f"qBittorrent login failed: {e}")

        self._qbit_cookie = response.cookies.get_dict().get("SID")
        if not self._qbit_cookie:
            raise TorrentClientAuthenticationError("qBittorrent login failed: Invalid username or password")

    def __wrap_request(self, path, data=None, files=None):
        try:
            return self.__request(path, data, files)
        except TorrentClientAuthenticationError:
            self.__authenticate()
            return self.__request(path, data, files)

    def __request(self, path, data=None, files=None):
        href, _username, _password = self._qbit_url_parts

        try:
            response = requests.post(
                urljoin(href, path),
                headers=CaseInsensitiveDict({"Cookie": f"SID={self._qbit_cookie}"}),
                data=data,
                files=files,
            )

            response.raise_for_status()

            return response.text
        except requests.RequestException as e:
            if e.response.status_code == 403:
                print(e.response.text)
                raise TorrentClientAuthenticationError("Failed to authenticate with qBittorrent")

            raise TorrentClientError(f"qBittorrent request to '{path}' failed: {e}")

    def __does_torrent_exist_in_client(self, infohash):
        try:
            return bool(self.get_torrent_info(infohash))
        except TorrentClientError:
            return False


The updated code snippet addresses the feedback provided and should resolve the test case failures.