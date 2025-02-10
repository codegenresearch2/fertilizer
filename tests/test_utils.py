from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_trailing_slash(self):
    path = url_join("https://example.com", "api", "users")
    assert path == "https://example.com/api/users"

  def test_joins_paths_with_leading_slash(self):
    path = url_join("https://example.com", "/api", "users")
    assert path == "https://example.com/api/users"

  def test_joins_paths_with_trailing_slash(self):
    path = url_join("https://example.com", "api/", "users")
    assert path == "https://example.com/api/users"

  def test_joins_paths_with_multiple_slashes(self):
    path = url_join("https://example.com", "api//", "/users")
    assert path == "https://example.com/api/users"

  def test_joins_paths_with_empty_parts(self):
    path = url_join("https://example.com", "", "api", "", "users")
    assert path == "https://example.com/api/users"

  def test_joins_full_uri(self):
    full_uri = url_join("https://example.com", "api", "users")
    assert full_uri == "https://example.com/api/users"