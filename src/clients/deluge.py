import json
import base64
import requests
from pathlib import Path
from requests.exceptions import RequestException, Timeout, ConnectionError
from requests.structures import CaseInsensitiveDict

from ..errors import TorrentClientError, TorrentClientAuthenticationError
from .torrent_client import TorrentClient

class Deluge(TorrentClient):
  def __init__(self, rpc_url):
    super().__init__()
    self._rpc_url = rpc_url
    self._deluge_cookie = None
    self._deluge_request_id = 0
    self._label_plugin_enabled = False

  def setup(self):
    try:
      connection_response = self.__authenticate()
    except TorrentClientAuthenticationError as auth_error:
      raise TorrentClientAuthenticationError(f"Failed to authenticate with Deluge: {auth_error}")

    self._label_plugin_enabled = self.__is_label_plugin_enabled()

    return connection_response

  def get_torrent_info(self, infohash):
    infohash = infohash.lower()
    params = [
      ["name", "state", "progress", "save_path", "label", "total_remaining"],
      {"hash": infohash},
    ]

    try:
      response = self.__request("web.update_ui", params)
    except TorrentClientAuthenticationError as auth_error:
      self._deluge_cookie = None
      self.__authenticate()
      response = self.__request("web.update_ui", params)

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

    new_torrent_infohash = self.__request("core.add_torrent_file", params)
    newtorrent_label = self.__determine_label(source_torrent_info)
    self.__set_label(new_torrent_infohash, newtorrent_label)

    return new_torrent_infohash

  def __authenticate(self):
    _href, _username, password = self._extract_credentials_from_url(self._rpc_url)
    if not password:
      raise TorrentClientAuthenticationError("You need to define a password in the Deluge RPC URL.")

    auth_response = self.__request("auth.login", [password])
    if not auth_response:
      raise TorrentClientAuthenticationError("Reached Deluge RPC endpoint but failed to authenticate")

    return self.__request("web.connected")

  def __is_label_plugin_enabled(self):
    response = self.__request("core.get_enabled_plugins")

    return "Label" in response

  def __determine_label(self, torrent_info):
    current_label = torrent_info.get("label")

    if not current_label or current_label == self.torrent_label:
      return self.torrent_label

    return f"{current_label}.{self.torrent_label}"

  def __set_label(self, infohash, label):
    if not self._label_plugin_enabled:
      return

    current_labels = self.__request("label.get_labels")
    if label not in current_labels:
      self.__request("label.add", [label])

    return self.__request("label.set_torrent", [infohash, label])

  def __request(self, method, params=[]):
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
    except Timeout:
      raise TorrentClientError(f"Deluge method {method} timed out after 10 seconds")
    except ConnectionError:
      raise TorrentClientError(f"Failed to connect to Deluge at {href}")

    try:
      json_response = response.json()
    except json.JSONDecodeError:
      raise TorrentClientError(f"Deluge method {method} response was non-JSON")

    self.__handle_response_headers(response.headers)

    if "error" in json_response and json_response["error"]:
      if json_response["error"]["code'] == 1:\n        raise TorrentClientAuthenticationError(f"Deluge method {method} returned an authentication error")\n      else:\n        raise TorrentClientError(f"Deluge method {method} returned an error: {json_response['error']}")\n\n    return json_response["result"]\n\n  def __handle_response_headers(self, headers):\n    if "Set-Cookie" in headers:\n      self._deluge_cookie = headers["Set-Cookie"].split(";")[0]