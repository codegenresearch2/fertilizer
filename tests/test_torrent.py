import os
import re
import pytest
import requests_mock

from .helpers import get_torrent_path, SetupTeardown

from src.trackers import RedTracker
from src.parser import get_bencoded_data, TorrentDecodingError
from src.errors import TorrentAlreadyExistsError, UnknownTrackerError, TorrentNotFoundError
from src.torrent import generate_new_torrent_from_file

class TestGenerateNewTorrentFromFile(SetupTeardown):
  def test_saves_new_torrent_from_red_to_ops(self, red_api, ops_api):
    with requests_mock.Mocker() as m:
      m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
      m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

      torrent_path = get_torrent_path("red_source")
      try:
        _, filepath, _ = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)
        parsed_torrent = get_bencoded_data(filepath)

        assert os.path.isfile(filepath)
        assert parsed_torrent[b"announce"] == b"https://home.opsfet.ch/bar/announce"
        assert parsed_torrent[b"comment"] == b"https://orpheus.network/torrents.php?torrentid=123"
        assert parsed_torrent[b"info"][b"source"] == b"OPS"

        os.remove(filepath)
      except TorrentDecodingError as e:
        pytest.fail(f"Unexpected TorrentDecodingError: {e}")

  # Rest of the tests follow the same pattern for error handling

  def test_raises_error_if_cannot_decode_torrent(self, red_api, ops_api):
    torrent_path = get_torrent_path("broken")
    with pytest.raises(TorrentDecodingError) as excinfo:
      generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)

    assert str(excinfo.value) == "Error decoding torrent file"

  # Rest of the tests follow the same pattern for error handling