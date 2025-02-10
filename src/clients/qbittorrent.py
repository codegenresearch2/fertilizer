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
        self._qbit_url, self._username, self._password = self._extract_credentials_from_url(qbit_url)
        self._qbit_cookie = None

    def setup(self):
        self.__authenticate()
        return self

    def get_torrent_info(self, infohash):
        response = self.__wrap_request("torrents/info", data={"hashes": infohash})
        if response is None:
            raise TorrentClientError("Client returned unexpected response")

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
        payload = {"username": self._username, "password": self._password} if self._username or self._password else {}

        try:
            response = requests.post(urljoin(self._qbit_url, "/api/v2/auth/login"), data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            raise TorrentClientAuthenticationError(f"qBittorrent login failed: {e}")

        self._qbit_cookie = response.cookies.get_dict().get("SID")
        if not self._qbit_cookie:
            raise TorrentClientAuthenticationError("qBittorrent login failed: Invalid username or password")

    def __wrap_request(self, path, data=None, files=None):
        try:
            return self.__perform_request(path, data, files)
        except TorrentClientAuthenticationError:
            self.__authenticate()
            return self.__perform_request(path, data, files)

    def __perform_request(self, path, data=None, files=None):
        try:
            response = requests.post(
                urljoin(self._qbit_url, path),
                headers=CaseInsensitiveDict({"Cookie": f"SID={self._qbit_cookie}"}),
                data=data,
                files=files,
            )

            response.raise_for_status()

            return response.text
        except requests.RequestException as e:
            if e.response.status_code == 403:
                raise TorrentClientAuthenticationError(f"Failed to authenticate with qBittorrent: {e.response.text}")

            raise TorrentClientError(f"qBittorrent request to '{path}' failed: {e}")

    def __does_torrent_exist_in_client(self, infohash):
        try:
            self.get_torrent_info(infohash)
            return True
        except TorrentClientError:
            return False

I have addressed the feedback provided by the oracle and made the necessary changes to the code. Here's the updated code snippet:

1. **Credential Extraction**: I have updated the `__init__` method to extract credentials from the URL using the same approach as the gold code.

2. **Response Handling**: In the `get_torrent_info` method, I have reordered the operations to check if the response is valid before parsing it.

3. **Variable Naming**: I have updated the variable name `new_torrent_already_exists` in the `inject_torrent` method to match the gold code's naming convention.

4. **Authentication Logic**: I have simplified the payload construction in the `__authenticate` method to handle empty credentials similarly to the gold code.

5. **Request Method Naming**: I have renamed the `__request` method to `__perform_request` to match the gold code's naming convention.

6. **Error Handling**: I have updated the error handling in the `__perform_request` method to provide clearer error messages when authentication fails.

7. **Use of Utility Functions**: I have used `urljoin` for URL handling as suggested.

These changes should enhance the alignment of the code with the gold standard.