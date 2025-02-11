import os
import pytest

from .helpers import get_torrent_path, SetupTeardown
from src.errors import TorrentDecodingError
from src.trackers import RedTracker, OpsTracker
from src.parser import (
  is_valid_infohash,
  get_source,
  get_name,
  get_bencoded_data,
  get_announce_url,
  get_origin_tracker,
  recalculate_hash_for_new_source,
  save_bencoded_data,
  calculate_infohash,
)

class TestIsValidInfohash(SetupTeardown):
  def test_returns_true_for_valid_infohash(self):
    assert is_valid_infohash("0beec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33"), "Expected valid infohash to return True"

  def test_returns_false_for_invalid_infohash(self):
    assert not is_valid_infohash("abc"), "Expected invalid infohash 'abc' to return False"
    assert not is_valid_infohash("mnopqrstuvwx"), "Expected invalid infohash 'mnopqrstuvwx' to return False"
    assert not is_valid_infohash("Ubeec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33"), "Expected invalid infohash 'Ubeec7b5ea3f0fdbc95d0dd47f3c5bc275da8a33' to return False"
    assert not is_valid_infohash(123), "Expected invalid infohash 123 to return False"

class TestGetSource(SetupTeardown):
  def test_returns_source_if_present(self):
    source = get_source({b"info": {b"source": b"FOO"}})
    assert source == b"FOO", f"Expected source 'FOO', but got {source}"

  def test_returns_none_if_absent(self):
    source = get_source({})
    assert source is None, f"Expected None, but got {source}"

class TestGetName(SetupTeardown):
  def test_returns_name_if_present(self):
    name = get_name({b"info": {b"name": b"foo"}})
    assert name == b"foo", f"Expected name 'foo', but got {name}"

  def test_returns_none_if_absent(self):
    name = get_name({})
    assert name is None, f"Expected None, but got {name}"

class TestGetAnnounceUrl(SetupTeardown):
  def test_returns_url_if_present_in_announce(self):
    url = get_announce_url({b"announce": b"https://foo.bar"})
    assert url == [b"https://foo.bar"], f"Expected URL ['https://foo.bar'], but got {url}"

  def test_returns_url_if_present_in_trackers(self):
    url = get_announce_url({b"trackers": [[b"https://foo.bar"], b"https://baz.qux"]})
    assert url == [b"https://foo.bar", b"https://baz.qux"], f"Expected URLs ['https://foo.bar', 'https://baz.qux'], but got {url}"

  def test_returns_none_if_absent(self):
    url = get_announce_url({})
    assert url is None, f"Expected None, but got {url}"

class TestGetOriginTracker(SetupTeardown):
  def test_returns_red_based_on_source(self):
    tracker = get_origin_tracker({b"info": {b"source": b"RED"}})
    assert tracker == RedTracker, f"Expected RedTracker, but got {tracker}"
    tracker = get_origin_tracker({b"info": {b"source": b"PTH"}})
    assert tracker == RedTracker, f"Expected RedTracker, but got {tracker}"

  def test_returns_ops_based_on_source(self):
    tracker = get_origin_tracker({b"info": {b"source": b"OPS"}})
    assert tracker == OpsTracker, f"Expected OpsTracker, but got {tracker}"

  def test_returns_red_based_on_announce(self):
    tracker = get_origin_tracker({b"announce": b"https://flacsfor.me/123abc"})
    assert tracker == RedTracker, f"Expected RedTracker, but got {tracker}"

  def test_returns_ops_based_on_announce(self):
    tracker = get_origin_tracker({b"announce": b"https://home.opsfet.ch/123abc"})
    assert tracker == OpsTracker, f"Expected OpsTracker, but got {tracker}"

  def test_returns_red_based_on_trackers(self):
    tracker = get_origin_tracker({b"trackers": [[b"https://flacsfor.me/123abc"], b"https://baz.qux"]})
    assert tracker == RedTracker, f"Expected RedTracker, but got {tracker}"

  def test_returns_ops_based_on_trackers(self):
    tracker = get_origin_tracker({b"trackers": [[b"https://home.opsfet.ch/123abc"], b"https://baz.qux"]})
    assert tracker == OpsTracker, f"Expected OpsTracker, but got {tracker}"

  def test_returns_none_if_no_match(self):
    tracker = get_origin_tracker({})
    assert tracker is None, f"Expected None, but got {tracker}"
    tracker = get_origin_tracker({b"info": {b"source": b"FOO"}})
    assert tracker is None, f"Expected None, but got {tracker}"
    tracker = get_origin_tracker({b"announce": b"https://foo/123abc"})
    assert tracker is None, f"Expected None, but got {tracker}"

class TestCalculateInfohash(SetupTeardown):
  def test_returns_infohash(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    infohash = calculate_infohash(torrent_data)
    assert infohash == "FD2F1D966DF7E2E35B0CF56BC8510C6BB4D44467", f"Expected infohash 'FD2F1D966DF7E2E35B0CF56BC8510C6BB4D44467', but got {infohash}"

  def test_raises_error_for_missing_info_key(self):
    torrent_data = {}
    with pytest.raises(TorrentDecodingError) as e:
      calculate_infohash(torrent_data)
    assert "Torrent data does not contain 'info' key" in str(e.value), f"Expected error message 'Torrent data does not contain 'info' key', but got {str(e.value)}"

class TestRecalculateHashForNewSource(SetupTeardown):
  def test_replaces_source_and_returns_hash(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    new_source = b"OPS"
    new_hash = recalculate_hash_for_new_source(torrent_data, new_source)
    assert new_hash == "4F36F59992B6F7CB6EB6C2DEE06DD66AC81A981B", f"Expected new hash '4F36F59992B6F7CB6EB6C2DEE06DD66AC81A981B', but got {new_hash}"

  def test_doesnt_mutate_original_dict(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    new_source = b"OPS"
    recalculate_hash_for_new_source(torrent_data, new_source)
    assert torrent_data == {b"info": {b"source": b"RED"}}, f"Expected original dict to remain unchanged, but got {torrent_data}"

class TestGetTorrentData(SetupTeardown):
  def test_returns_torrent_data(self):
    torrent_data = get_bencoded_data(get_torrent_path("no_source"))
    assert isinstance(torrent_data, dict), f"Expected dict, but got {type(torrent_data)}"
    assert b"info" in torrent_data, f"Expected 'info' key in torrent data, but got {torrent_data}"

  def test_returns_none_on_error(self):
    torrent_data = get_bencoded_data(get_torrent_path("broken"))
    assert torrent_data is None, f"Expected None, but got {torrent_data}"

class TestSaveTorrentData(SetupTeardown):
  def test_saves_torrent_data(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    filename = "/tmp/test_save_bencoded_data.torrent"
    save_bencoded_data(filename, torrent_data)
    with open(filename, "rb") as f:
      saved_data = f.read()
    assert saved_data == b"d4:infod6:source3:REDee", f"Expected saved data 'd4:infod6:source3:REDee', but got {saved_data}"
    os.remove(filename)

  def test_returns_filename(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    filename = "/tmp/test_save_bencoded_data.torrent"
    saved_filename = save_bencoded_data(filename, torrent_data)
    assert saved_filename == filename, f"Expected filename '{filename}', but got {saved_filename}"
    os.remove(filename)

  def test_creates_parent_directory(self):
    torrent_data = {b"info": {b"source": b"RED"}}
    filename = "/tmp/output/foo/test_save_bencoded_data.torrent"
    save_bencoded_data(filename, torrent_data)
    assert os.path.exists("/tmp/output/foo"), f"Expected directory '/tmp/output/foo' to exist, but it does not"
    os.remove(filename)