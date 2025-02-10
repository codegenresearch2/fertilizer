import os
import re
import pytest
import requests_mock

from .helpers import get_torrent_path, SetupTeardown, copy_and_mkdir

from src.trackers import RedTracker
from src.parser import get_bencoded_data
from src.errors import TorrentAlreadyExistsError, TorrentDecodingError, UnknownTrackerError, TorrentNotFoundError
from src.torrent import generate_new_torrent_from_file

# Comment added to provide context for the test
def test_saves_new_torrent_from_red_to_ops(red_api, ops_api):
    with requests_mock.Mocker() as m:
        m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
        m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

        torrent_path = get_torrent_path("red_source")
        _, filepath, _ = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)
        parsed_torrent = get_bencoded_data(filepath)

        assert os.path.isfile(filepath), "Expected the new torrent file to be saved"
        assert parsed_torrent[b"announce"] == b"https://home.opsfet.ch/bar/announce", "Expected the announce URL to be set correctly"
        assert parsed_torrent[b"comment"] == b"https://orpheus.network/torrents.php?torrentid=123", "Expected the comment to be set correctly"
        assert parsed_torrent[b"info"][b"source"] == b"OPS", "Expected the source to be set to OPS"

        os.remove(filepath)

# Adding a test for a specific error case
def test_raises_error_if_torrent_has_no_info(red_api, ops_api):
    with pytest.raises(TorrentDecodingError, match="Error decoding torrent file"):
        torrent_path = get_torrent_path("no_info")
        generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)

# Ensuring the use of helper functions
def test_returns_appropriately_if_torrent_already_exists(red_api, ops_api):
    filepath = "/tmp/OPS/foo [OPS].torrent"
    copy_and_mkdir(get_torrent_path("ops_source"), filepath)

    with requests_mock.Mocker() as m:
        m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
        m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

        torrent_path = get_torrent_path("red_source")
        _, _, previously_generated = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)

    assert previously_generated, "Expected the torrent to already exist"
    os.remove(filepath)

# Adding assertion messages for clarity
def test_raises_error_if_api_response_error(red_api, ops_api):
    with pytest.raises(TorrentNotFoundError, match="Torrent could not be found on OPS"):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_KNOWN_BAD_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("red_source")
            generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)

# Ensuring consistent formatting and indentation
class TestGenerateNewTorrentFromFile(SetupTeardown):
    def test_saves_new_torrent_from_red_to_ops(self, red_api, ops_api):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("red_source")
            _, filepath, _ = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)
            parsed_torrent = get_bencoded_data(filepath)

            assert os.path.isfile(filepath), "Expected the new torrent file to be saved"
            assert parsed_torrent[b"announce"] == b"https://home.opsfet.ch/bar/announce", "Expected the announce URL to be set correctly"
            assert parsed_torrent[b"comment"] == b"https://orpheus.network/torrents.php?torrentid=123", "Expected the comment to be set correctly"
            assert parsed_torrent[b"info"][b"source"] == b"OPS", "Expected the source to be set to OPS"

            os.remove(filepath)