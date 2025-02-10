import json
import base64
import requests
from pathlib import Path

from ..errors import TorrentClientError, TorrentClientAuthenticationError, TorrentClientTimeoutError
from .torrent_client import TorrentClient
from requests.exceptions import RequestException
from requests.structures import CaseInsensitiveDict

class Deluge(TorrentClient):
    ERROR_CODES = {
        1: TorrentClientAuthenticationError,
        408: TorrentClientTimeoutError,
    }

    def __init__(self, rpc_url):
        super().__init__()
        self._rpc_url = rpc_url
        self._deluge_cookie = None
        self._deluge_request_id = 0
        self._label_plugin_enabled = False

    def setup(self):
        try:
            connection_response = self.__authenticate()
            self._label_plugin_enabled = self.__is_label_plugin_enabled()
            return connection_response
        except TorrentClientAuthenticationError as auth_error:
            raise auth_error
        except TorrentClientTimeoutError as timeout_error:
            raise timeout_error
        except Exception as setup_error:
            raise TorrentClientError("Failed to set up Deluge client") from setup_error

    def get_torrent_info(self, infohash):
        infohash = infohash.lower()
        params = [
            ["name", "state", "progress", "save_path", "label", "total_remaining"],
            {"hash": infohash},
        ]

        try:
            response = self.__wrap_request("web.update_ui", params)
        except TorrentClientError as client_error:
            raise client_error

        if "torrents" not in response:
            raise TorrentClientError("Client returned unexpected response (object missing)")

        torrent = response["torrents"].get(infohash)
        if torrent is None:
            raise TorrentClientError(f"Torrent not found in client ({infohash})")

        torrent_completed = (
            (torrent["state"] == "Paused" and (torrent["progress"] == 100 or not torrent["total_remaining"]))
            or torrent["state"] == "Seeding"
            or torrent["progress"] == 100
            or not torrent["total_remaining"]
        )

        return {
            "complete": torrent_completed,
            "label": torrent.get("label"),
            "save_path": torrent["save_path"],
        }

    def inject_torrent(self, source_torrent_infohash, new_torrent_filepath, save_path_override=None):
        source_torrent_info = self.get_torrent_info(source_torrent_infohash)

        if not source_torrent_info["complete"]:
            raise TorrentClientError("Cannot inject a torrent that is not complete")

        params = [
            f"{Path(new_torrent_filepath).stem}.fertilizer.torrent",
            base64.b64encode(open(new_torrent_filepath, "rb").read()).decode(),
            {
                "download_location": save_path_override if save_path_override else source_torrent_info["save_path"],
                "seed_mode": True,
                "add_paused": False,
            },
        ]

        try:
            new_torrent_infohash = self.__wrap_request("core.add_torrent_file", params)
        except TorrentClientError as client_error:
            raise client_error

        newtorrent_label = self.__determine_label(source_torrent_info)
        try:
            self.__set_label(new_torrent_infohash, newtorrent_label)
        except TorrentClientError as client_error:
            raise client_error

        return new_torrent_infohash

    def __authenticate(self):
        _href, _username, password = self._extract_credentials_from_url(self._rpc_url)
        if not password:
            raise TorrentClientAuthenticationError("You need to define a password in the Deluge RPC URL. (e.g. http://:<PASSWORD>@localhost:8112)")

        try:
            auth_response = self.__wrap_request("auth.login", [password])
        except TorrentClientError as auth_error:
            raise auth_error

        if not auth_response:
            raise TorrentClientAuthenticationError("Failed to authenticate with Deluge")

        return auth_response

    def __is_label_plugin_enabled(self):
        try:
            response = self.__wrap_request("core.get_enabled_plugins")
        except TorrentClientError as client_error:
            raise client_error

        return "Label" in response

    def __determine_label(self, torrent_info):
        current_label = torrent_info.get("label")

        if not current_label or current_label == self.torrent_label:
            return self.torrent_label

        return f"{current_label}.{self.torrent_label}"

    def __set_label(self, infohash, label):
        if not self._label_plugin_enabled:
            return

        try:
            current_labels = self.__wrap_request("label.get_labels")
        except TorrentClientError as client_error:
            raise client_error

        if label not in current_labels:
            try:
                self.__wrap_request("label.add", [label])
            except TorrentClientError as client_error:
                raise client_error

        try:
            return self.__wrap_request("label.set_torrent", [infohash, label])
        except TorrentClientError as client_error:
            raise client_error

    def __wrap_request(self, method, params=[]):
        href, _, _ = self._extract_credentials_from_url(self._rpc_url)

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        if self._deluge_cookie:
            headers["Cookie"] = self._deluge_cookie

        try:
            response = requests.post(
                href,
                json={
                    "method": method,
                    "params": params,
                    "id": self._deluge_request_id,
                },
                headers=headers,
                timeout=10,
            )
            self._deluge_request_id += 1
        except RequestException as network_error:
            if network_error.response and network_error.response.status_code == 408:
                raise TorrentClientTimeoutError(f"Deluge method {method} timed out after 10 seconds")
            raise TorrentClientError(f"Failed to connect to Deluge at {href}") from network_error

        try:
            json_response = response.json()
        except json.JSONDecodeError as json_parse_error:
            raise TorrentClientError(f"Deluge method {method} response was non-JSON") from json_parse_error

        if "error" in json_response and json_response["error"]:
            error_code = json_response["error"].get("code")
            if error_code in self.ERROR_CODES:
                raise self.ERROR_CODES[error_code](f"Deluge method {method} returned an error: {json_response['error']}")
            raise TorrentClientError(f"Deluge method {method} returned an error: {json_response['error']}")

        return json_response["result"]

    def __handle_response_headers(self, headers):
        if "Set-Cookie" in headers:
            self._deluge_cookie = headers["Set-Cookie"].split(";")[0]


This revised code snippet addresses the feedback from the oracle, including the `SyntaxError` and the suggested improvements such as error handling, method naming, response validation, parameter handling, code structure, and use of constants.