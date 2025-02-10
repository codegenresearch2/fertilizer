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
    assert RedTracker.announce_url() == RedAPI().announce_url
    assert OpsTracker.announce_url() == OpsAPI().announce_url

  def test_site_shortname(self):
    assert RedTracker.site_shortname() == "RED"
    assert OpsTracker.site_shortname() == "OPS"

  def test_reciprocal_tracker(self):
    assert RedTracker.reciprocal_tracker() == OpsTracker
    assert OpsTracker.reciprocal_tracker() == RedTracker

  def test_filepath_generation(self):
    # Simplified filepath generation logic
    site_shortname = RedTracker.site_shortname()
    torrent_hash = "example_hash"
    filepath = f"/path/to/save/{site_shortname}/{torrent_hash}.torrent"
    assert filepath == "/path/to/save/RED/example_hash.torrent"