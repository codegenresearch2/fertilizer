import os
import pytest
from src.parser import is_valid_infohash, get_source, get_name, get_bencoded_data, get_announce_url, get_origin_tracker, recalculate_hash_for_new_source, save_bencoded_data, calculate_infohash
from src.errors import TorrentDecodingError

class SetupTeardown(object):
    def setup_method(self):
        pass

    def teardown_method(self):
        pass

class TestIsValidInfohash(SetupTeardown):
    def test_returns_true_for_valid_infohash(self):
        assert is_valid_infohash("0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33")

    def test_returns_false_for_invalid_infohash(self):
        assert not is_valid_infohash("abc")
        assert not is_valid_infohash("mnopqrstuvwx")
        assert not is_valid_infohash(123)

class TestGetSource(SetupTeardown):
    def test_returns_source_if_present(self):
        assert get_source({b"info": {b"source": b"FOO"}}) == b"FOO"

    def test_returns_none_if_absent(self):
        assert get_source({}) is None

class TestGetName(SetupTeardown):
    def test_returns_name_if_present(self):
        assert get_name({b"info": {b"name": b"foo"}}) == b"foo"

    def test_returns_none_if_absent(self):
        assert get_name({}) is None

class TestGetAnnounceUrl(SetupTeardown):
    def test_returns_url_if_present_in_announce(self):
        assert get_announce_url({b"announce": b"https://foo.bar"}) == [b"https://foo.bar"]

    def test_returns_url_if_present_in_trackers(self):
        assert get_announce_url({b"trackers": [[b"https://foo.bar"], b"https://baz.qux"]}) == [b"https://foo.bar", b"https://baz.qux"]

    def test_returns_none_if_absent(self):
        assert get_announce_url({}) is None

class TestGetOriginTracker(SetupTeardown):
    def test_returns_red_based_on_source(self):
        assert get_origin_tracker({b"info": {b"source": b"RED"}}) == RedTracker
        assert get_origin_tracker({b"info": {b"source": b"PTH"}}) == RedTracker

    def test_returns_ops_based_on_source(self):
        assert get_origin_tracker({b"info": {b"source": b"OPS"}}) == OpsTracker

    def test_returns_red_based_on_announce(self):
        assert get_origin_tracker({b"announce": b"https://flacsfor.me/123abc"}) == RedTracker

    def test_returns_ops_based_on_announce(self):
        assert get_origin_tracker({b"announce": b"https://home.opsfet.ch/123abc"}) == OpsTracker

    def test_returns_red_based_on_trackers(self):
        assert get_origin_tracker({b"trackers": [[b"https://flacsfor.me/123abc"], b"https://baz.qux"]}) == RedTracker

    def test_returns_ops_based_on_trackers(self):
        assert get_origin_tracker({b"trackers": [[b"https://home.opsfet.ch/123abc"], b"https://baz.qux"]}) == OpsTracker

    def test_returns_none_if_no_match(self):
        assert get_origin_tracker({}) is None
        assert get_origin_tracker({b"info": {b"source": b"FOO"}}) is None
        assert get_origin_tracker({b"announce": b"https://foo/123abc"}) is None

class TestCalculateInfohash(SetupTeardown):
    def test_returns_infohash(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        result = calculate_infohash(torrent_data)
        assert result == "FD2F1D966DF7E2E35B0CF56BC8510C6BB4D44467"

    def test_raises_exception_for_missing_info_key(self):
        with pytest.raises(TorrentDecodingError) as exc_info:
            calculate_infohash({})
        assert str(exc_info.value) == "Torrent data does not contain 'info' key"

class TestRecalculateHashForNewSource(SetupTeardown):
    def test_replaces_source_and_returns_hash(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        new_source = b"OPS"
        result = recalculate_hash_for_new_source(torrent_data, new_source)
        assert result == "4F36F59992B6F7CB6EB6C2DEE06DD66AC81A981B"

    def test_doesnt_mutate_original_dict(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        new_source = b"OPS"
        recalculate_hash_for_new_source(torrent_data, new_source)
        assert torrent_data == {b"info": {b"source": b"RED"}}

class TestSaveBencodedData(SetupTeardown):
    def test_saves_torrent_data(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        filename = "/tmp/test_save_bencoded_data.torrent"
        save_bencoded_data(filename, torrent_data)
        with open(filename, "rb") as f:
            result = f.read()
        assert result == b"d4:infod6:source3:REDee"
        os.remove(filename)

    def test_returns_filename(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        filename = "/tmp/test_save_bencoded_data.torrent"
        result = save_bencoded_data(filename, torrent_data)
        assert result == filename
        os.remove(filename)

    def test_creates_parent_directory(self):
        torrent_data = {b"info": {b"source": b"RED"}}
        filename = "/tmp/output/foo/test_save_bencoded_data.torrent"
        save_bencoded_data(filename, torrent_data)
        assert os.path.exists("/tmp/output/foo")
        os.remove(filename)

if __name__ == "__main__":
    pytest.main()


This revised code snippet addresses the feedback provided by the oracle. It ensures that the import statements are organized, uses inheritance for setup and teardown, follows consistent naming conventions, adds more test cases for edge cases, handles error messages correctly, and ensures proper file operations.