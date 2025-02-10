from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    result = url_join("https://example.com", "api", "users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_leading_slash(self):
    result = url_join("https://example.com", "/api", "users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_trailing_slash(self):
    result = url_join("https://example.com", "api/", "users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_multiple_slashes(self):
    result = url_join("https://example.com", "api//", "/users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_empty_parts(self):
    result = url_join("https://example.com", "", "api", "", "users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_stripped_slashes(self):
    result = url_join("https://example.com", "/api/", "/users/")
    assert result == "https://example.com/api/users"

  def test_joins_full_uri_with_path(self):
    result = url_join("https://example.com/", "api", "users")
    assert result == "https://example.com/api/users"

  def test_joins_paths_with_query_string(self):
    result = url_join("https://example.com", "api", "users?page=1")
    assert result == "https://example.com/api/users?page=1"