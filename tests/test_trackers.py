from .helpers import SetupTeardown
from src.trackers import RedTracker, OpsTracker

class TestTrackerMethods(SetupTeardown):
  def test_source_flags_for_search(self):
    # Ensure the source flags for search are correct
    assert RedTracker.source_flags_for_search() == [b"RED", b"PTH"]
    assert OpsTracker.source_flags_for_search() == [b"OPS", b"APL"]

  def test_source_flags_for_creation(self):
    # Ensure the source flags for creation are correct
    assert RedTracker.source_flags_for_creation() == [b"RED", b"PTH", b""]
    assert OpsTracker.source_flags_for_creation() == [b"OPS", b"APL", b""]

  def test_announce_url(self):
    # Ensure the announce URLs are correct
    assert RedTracker.announce_url() == b"flacsfor.me"
    assert OpsTracker.announce_url() == b"home.opsfet.ch"

  def test_site_shortname(self):
    # Ensure the site shortnames are correct
    assert RedTracker.site_shortname() == "RED"
    assert OpsTracker.site_shortname() == "OPS"

  def test_reciprocal_tracker(self):
    # Ensure the reciprocal trackers are correct
    assert RedTracker.reciprocal_tracker() == OpsTracker
    assert OpsTracker.reciprocal_tracker() == RedTracker