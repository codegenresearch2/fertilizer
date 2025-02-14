import json
import base64
import requests
from pathlib import Path
from requests import HTTPError, Timeout, ConnectionError

from ..errors import TorrentClientError, TorrentClientAuthenticationError
from .torrent_client import TorrentClient
from requests.structures import CaseInsensitiveDict

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
      self._label_plugin_enabled = self.__is_label_plugin_enabled()
      return connection_response
    except TorrentClientAuthenticationError as auth_error:
      raise TorrentClientAuthenticationError("Failed to set up Deluge client: " + str(auth_error))
    except Exception as error:
      raise TorrentClientError("Failed to set up Deluge client: " + str(error))

  def get_torrent_info(self, infohash):
    infohash = infohash.lower()
    params = [
      [
        "name",
        "state",
        "progress",
        "save_path",
        "label",
        "total_remaining",
      ],
      {"hash": infohash},
    ]

    try:
      response = self.__request("web.update_ui", params)
      if "torrents" in response:
        torrent = response["torrents"].get(infohash)
        if torrent is None:
          raise TorrentClientError(f"Torrent not found in client ({infohash})")
      else:
        raise TorrentClientError("Client returned unexpected response (object missing)")

      torrent_completed = self.__check_torrent_completion(torrent)
      return {
        "complete": torrent_completed,
        "label": torrent.get("label"),
        "save_path": torrent["save_path"],
      }
    except TorrentClientAuthenticationError as auth_error:
      raise TorrentClientAuthenticationError("Failed to get torrent info: " + str(auth_error))
    except Exception as error:
      raise TorrentClientError("Failed to get torrent info: " + str(error))

  def inject_torrent(self, source_torrent_infohash, new_torrent_filepath, save_path_override=None):
    try:
      source_torrent_info = self.get_torrent_info(source_torrent_infohash)
      if not source_torrent_info["complete"]:
        raise TorrentClientError("Cannot inject a torrent that is not complete")

      params = self.__prepare_inject_torrent_params(new_torrent_filepath, source_torrent_info, save_path_override)
      new_torrent_infohash = self.__request("core.add_torrent_file", params)
      newtorrent_label = self.__determine_label(source_torrent_info)
      self.__set_label(new_torrent_infohash, newtorrent_label)

      return new_torrent_infohash
    except TorrentClientAuthenticationError as auth_error:
      raise TorrentClientAuthenticationError("Failed to inject torrent: " + str(auth_error))
    except Exception as error:
      raise TorrentClientError("Failed to inject torrent: " + str(error))

  # Rest of the code remains unchanged