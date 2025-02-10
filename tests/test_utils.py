from .helpers import SetupTeardown
from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    assert url_join("https://example.com", "api", "users") == "https://example.com/api/users"

  def test_joins_paths_with_leading_slash(self):
    assert url_join("https://example.com", "/api", "users") == "https://example.com/api/users"

  def test_joins_paths_with_trailing_slash(self):
    assert url_join("https://example.com", "api/", "users") == "https://example.com/api/users"

  def test_joins_paths_with_multiple_slashes(self):
    assert url_join("https://example.com", "api//", "/users") == "https://example.com/api/users"

  def test_joins_paths_with_empty_parts(self):
    assert url_join("https://example.com", "", "api", "", "users") == "https://example.com/api/users"

  def test_joins_paths_with_stripping(self):
    assert url_join("https://example.com/", "/api/", "/users/") == "https://example.com/api/users"