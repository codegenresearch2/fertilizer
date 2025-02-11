import os
import re
import shutil
import pytest
import requests_mock

from unittest.mock import MagicMock
from colorama import Fore

from .helpers import SetupTeardown, get_torrent_path, copy_and_mkdir

from src.errors import TorrentExistsInClientError
from src.scanner import scan_torrent_directory, scan_torrent_file


class TestScanTorrentFile:
    def test_handles_missing_torrent_file(self, red_api, ops_api):
        with pytest.raises(FileNotFoundError):
            scan_torrent_file("/tmp/nonexistent.torrent", "/tmp/output", red_api, ops_api, None)

    def test_creates_output_directory_if_nonexistent(self, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        shutil.rmtree("/tmp/new_output", ignore_errors=True)

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_file("/tmp/input/red_source.torrent", "/tmp/new_output", red_api, ops_api, None)

        assert os.path.isdir("/tmp/new_output")
        shutil.rmtree("/tmp/new_output")

    def test_returns_generated_torrent_filepath(self, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            filepath = scan_torrent_file("/tmp/input/red_source.torrent", "/tmp/output", red_api, ops_api, None)

            assert os.path.isfile(filepath)
            assert filepath == "/tmp/output/OPS/foo [OPS].torrent"

    def test_calls_injector_if_provided(self, red_api, ops_api):
        injector_mock = MagicMock()
        injector_mock.inject_torrent = MagicMock()
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_file("/tmp/input/red_source.torrent", "/tmp/output", red_api, ops_api, injector_mock)

        injector_mock.inject_torrent.assert_called_once_with(
            "/tmp/input/red_source.torrent", "/tmp/output/OPS/foo [OPS].torrent", "OPS"
        )

    def test_handles_duplicate_torrents(self, red_api, ops_api):
        injector_mock = MagicMock()
        injector_mock.inject_torrent = MagicMock()
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("ops_source"), "/tmp/output/ops_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_file("/tmp/input/red_source.torrent", "/tmp/output", red_api, ops_api, injector_mock)

        injector_mock.inject_torrent.assert_called_once_with(
            "/tmp/input/red_source.torrent", "/tmp/output/ops_source.torrent", "OPS"
        )

    def test_handles_torrents_with_bad_encoding(self, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("broken_name"), "/tmp/output/broken_name.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_file("/tmp/input/red_source.torrent", "/tmp/output", red_api, ops_api, None)


class TestScanTorrentDirectory:
    def test_handles_missing_input_directory(self, red_api, ops_api):
        with pytest.raises(FileNotFoundError):
            scan_torrent_directory("/tmp/nonexistent", "/tmp/output", red_api, ops_api, None)

    def test_creates_output_directory_if_nonexistent(self, red_api, ops_api):
        shutil.rmtree("/tmp/new_output", ignore_errors=True)
        scan_torrent_directory("/tmp/input", "/tmp/new_output", red_api, ops_api, None)

        assert os.path.isdir("/tmp/new_output")
        shutil.rmtree("/tmp/new_output")

    def test_lists_generated_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "Found with source 'OPS' and generated as '/tmp/output/OPS/foo [OPS].torrent'." in captured.out
            assert "Generated for cross-seeding: 1" in captured.out

    def test_lists_undecodable_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("broken"), "/tmp/input/broken.torrent")

        scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
        captured = capsys.readouterr()

        assert "Error decoding torrent file" in captured.out
        assert "Errors: 1" in captured.out

    def test_lists_unknown_tracker_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("no_source"), "/tmp/input/no_source.torrent")

        scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
        captured = capsys.readouterr()

        assert "Torrent not from OPS or RED based on source or announce URL" in captured.out
        assert "Skipped: 1" in captured.out

    def test_lists_already_existing_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/output/OPS/foo [OPS].torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "Torrent was previously generated." in captured.out
            assert "Already exists: 1" in captured.out

    def test_considers_matching_input_torrents_as_already_existing(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("ops_source"), "/tmp/input/ops_source.torrent")

        scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
        captured = capsys.readouterr()

        assert "Torrent already exists in input directory at /tmp/input/red_source.torrent" in captured.out
        assert "Already exists: 2" in captured.out

    def test_considers_matching_output_torrents_as_already_existing(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("ops_source"), "/tmp/output/ops_source.torrent")

        scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
        captured = capsys.readouterr()

        assert "Torrent was previously generated." in captured.out
        assert "Already exists: 1" in captured.out

    def test_lists_torrents_that_already_exist_in_client(self, capsys, red_api, ops_api):
        injector_mock = MagicMock()
        injector_mock.inject_torrent = MagicMock()
        injector_mock.inject_torrent.side_effect = TorrentExistsInClientError("Torrent exists in client")
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, injector_mock)
            captured = capsys.readouterr()

            assert "Torrent exists in client" in captured.out
            assert "Already exists: 1" in captured.out

    def test_lists_not_found_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "not_found"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "Torrent could not be found on OPS" in captured.out
            assert "Not found: 1" in captured.out

    def test_lists_unknown_error_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "unknown_error"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "An unknown error occurred in the API response from OPS" in captured.out
            assert "Errors: 1" in captured.out

    def test_reports_progress_for_mix_of_torrents(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("ops_announce"), "/tmp/input/ops_announce.torrent")
        copy_and_mkdir(get_torrent_path("no_source"), "/tmp/input/no_source.torrent")
        copy_and_mkdir(get_torrent_path("broken"), "/tmp/input/broken.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "Analyzed 3 local torrents" in captured.out

            assert "Found with source 'RED' and generated as '/tmp/output/RED/foo [RED].torrent'." in captured.out
            assert "Generated for cross-seeding: 1" in captured.out

            assert "Torrent not from OPS or RED based on source or announce URL" in captured.out
            assert "Skipped: 1" in captured.out

            assert "Error decoding torrent file" in captured.out
            assert "Errors: 1" in captured.out

    def test_doesnt_care_about_other_files_in_input_directory(self, capsys, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/non-torrent.txt")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)
            captured = capsys.readouterr()

            assert "Analyzed 0 local torrents" in captured.out

    def test_calls_injector_if_provided(self, red_api, ops_api):
        injector_mock = MagicMock()
        injector_mock.inject_torrent = MagicMock()
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, injector_mock)

        injector_mock.inject_torrent.assert_called_once_with(
            "/tmp/input/red_source.torrent", "/tmp/output/OPS/foo [OPS].torrent", "OPS"
        )

    def test_handles_torrents_with_bad_encoding(self, red_api, ops_api):
        copy_and_mkdir(get_torrent_path("red_source"), "/tmp/input/red_source.torrent")
        copy_and_mkdir(get_torrent_path("broken_name"), "/tmp/input/broken_name.torrent")

        with requests_mock.Mocker() as m:
            m.get(re.compile("action=torrent"), json={"status": "success"})
            m.get(re.compile("action=index"), json={"status": "success"})

            scan_torrent_directory("/tmp/input", "/tmp/output", red_api, ops_api, None)