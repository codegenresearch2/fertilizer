from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_with_empty_last_segment(self):
    result = url_join("https://example.com", "api", "")
    assert result == "https://example.com/api/", f"Expected 'https://example.com/api/', but got {result}"

  def test_joins_paths_with_single_segment_without_trailing_slash(self):
    result = url_join("https://example.com", "api")
    assert result == "https://example.com/api", f"Expected 'https://example.com/api', but got {result}"

  def test_joins_paths_with_trailing_slash_in_last_segment(self):
    result = url_join("https://example.com", "api", "users/")
    assert result == "https://example.com/api/users/", f"Expected 'https://example.com/api/users/', but got {result}"

  def test_joins_paths_with_multiple_segments(self):
    result = url_join("https://example.com", "api", "users", "profile")
    assert result == "https://example.com/api/users/profile", f"Expected 'https://example.com/api/users/profile', but got {result}"