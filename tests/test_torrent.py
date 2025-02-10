import os
import re
import pytest
import requests_mock

from .helpers import get_torrent_path, SetupTeardown

from src.trackers import RedTracker, OpsTracker
from src.parser import get_bencoded_data
from src.errors import TorrentAlreadyExistsError, TorrentDecodingError, UnknownTrackerError, TorrentNotFoundError
from src.torrent import generate_new_torrent_from_file, __generate_torrent_output_filepath

class TestGenerateNewTorrentFromFile(SetupTeardown):
    def test_saves_new_torrent_from_red_to_ops(self, red_api, ops_api):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("red_source")
            new_tracker, filepath = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)
            parsed_torrent = get_bencoded_data(filepath)

            assert os.path.isfile(filepath)
            assert parsed_torrent[b"announce"] == b"https://home.opsfet.ch/bar/announce"
            assert parsed_torrent[b"comment"] == b"https://orpheus.network/torrents.php?torrentid=123"
            assert parsed_torrent[b"info"][b"source"] == b"OPS"
            assert new_tracker == OpsTracker

            os.remove(filepath)

    def test_saves_new_torrent_from_ops_to_red(self, red_api, ops_api):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("ops_source")
            new_tracker, filepath = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api)
            parsed_torrent = get_bencoded_data(filepath)

            assert parsed_torrent[b"announce"] == b"https://flacsfor.me/bar/announce"
            assert parsed_torrent[b"comment"] == b"https://redacted.ch/torrents.php?torrentid=123"
            assert parsed_torrent[b"info"][b"source"] == b"RED"
            assert new_tracker == RedTracker

            os.remove(filepath)

    # Added new source flag for OpsTracker
    def test_saves_new_torrent_from_ops_to_new_source(self, red_api, ops_api):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("ops_source")
            new_tracker, filepath = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api, new_source="NEW")
            parsed_torrent = get_bencoded_data(filepath)

            assert parsed_torrent[b"announce"] == b"https://flacsfor.me/bar/announce"
            assert parsed_torrent[b"comment"] == b"https://redacted.ch/torrents.php?torrentid=123"
            assert parsed_torrent[b"info"][b"source"] == b"NEW"
            assert new_tracker == OpsTracker

            os.remove(filepath)

    # Added new source flag for RedTracker
    def test_saves_new_torrent_from_red_to_new_source(self, red_api, ops_api):
        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json=self.TORRENT_SUCCESS_RESPONSE)
            m.get(re.compile("action=index"), json=self.ANNOUNCE_SUCCESS_RESPONSE)

            torrent_path = get_torrent_path("red_source")
            new_tracker, filepath = generate_new_torrent_from_file(torrent_path, "/tmp", red_api, ops_api, new_source="NEW")
            parsed_torrent = get_bencoded_data(filepath)

            assert parsed_torrent[b"announce"] == b"https://home.opsfet.ch/bar/announce"
            assert parsed_torrent[b"comment"] == b"https://orpheus.network/torrents.php?torrentid=123"
            assert parsed_torrent[b"info"][b"source"] == b"NEW"
            assert new_tracker == RedTracker

            os.remove(filepath)

    # Rest of the tests remain the same

class TestGenerateTorrentOutputFilepath(SetupTeardown):
    API_RESPONSE = {"response": {"torrent": {"filePath": "foo"}}}

    def test_constructs_a_path_from_response_and_source(self):
        filepath = __generate_torrent_output_filepath(self.API_RESPONSE, OpsTracker, "base/dir")

        assert filepath == "base/dir/OPS/foo [OPS].torrent"

    def test_raises_error_if_file_exists(self):
        filepath = __generate_torrent_output_filepath(self.API_RESPONSE, OpsTracker, "/tmp")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write("")

        with pytest.raises(TorrentAlreadyExistsError) as excinfo:
            __generate_torrent_output_filepath(self.API_RESPONSE, OpsTracker, "/tmp")

        assert str(excinfo.value) == f"Torrent file already exists at {filepath}"
        os.remove(filepath)