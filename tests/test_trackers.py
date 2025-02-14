from .helpers import SetupTeardown
from src.trackers import RedTracker, OpsTracker
from src.api import RedAPI, OpsAPI

class TestTrackerMethods(SetupTeardown):
  def test_source_flags_for_search(self):
    assert RedTracker.source_flags_for_search() == [b"RED", b"PTH"]
    assert OpsTracker.source_flags_for_search() == [b"OPS", b"APL"]

  def test_source_flags_for_creation(self):
    assert RedTracker.source_flags_for_creation() == [b"RED", b"PTH", b""]
    assert OpsTracker.source_flags_for_creation() == [b"OPS", b"APL", b""]

  def test_announce_url(self):
    red_api = RedAPI("dummy_key")
    ops_api = OpsAPI("dummy_key")
    assert RedTracker.announce_url() == red_api.announce_url.encode()
    assert OpsTracker.announce_url() == ops_api.announce_url.encode()

  def test_site_shortname(self):
    assert RedTracker.site_shortname() == "RED"
    assert OpsTracker.site_shortname() == "OPS"

  def test_reciprocal_tracker(self):
    assert RedTracker.reciprocal_tracker() == OpsTracker
    assert OpsTracker.reciprocal_tracker() == RedTracker

  def test_filepath_generation(self):
    # Simplified filepath generation example
    torrent_hash = "dummy_hash"
    red_api = RedAPI("dummy_key")
    torrent_info = red_api.find_torrent(torrent_hash)
    filepath = f"{torrent_info['group_name']}/{torrent_info['torrent_name']}"
    print(filepath)