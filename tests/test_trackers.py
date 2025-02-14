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
    assert RedTracker.announce_url() == red_api.announce_url
    assert OpsTracker.announce_url() == ops_api.announce_url

  def test_site_shortname(self):
    assert RedTracker.site_shortname() == "RED"
    assert OpsTracker.site_shortname() == "OPS"

  def test_reciprocal_tracker(self):
    assert RedTracker.reciprocal_tracker() == OpsTracker
    assert OpsTracker.reciprocal_tracker() == RedTracker

  def test_consistent_api_response(self):
    red_api = RedAPI("dummy_key")
    ops_api = OpsAPI("dummy_key")
    assert "status" in red_api.get_account_info()
    assert "status" in ops_api.get_account_info()

  def test_simplified_output_filepath(self):
    # Assuming a simple function to generate filepath
    def generate_filepath(tracker):
      return f"/data/{tracker.site_shortname()}/torrents"

    assert generate_filepath(RedTracker) == "/data/RED/torrents"
    assert generate_filepath(OpsTracker) == "/data/OPS/torrents"