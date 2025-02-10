from .helpers import SetupTeardown
from src.utils import url_join, flatten

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

class TestUrlJoin:
  def test_joins_paths(self):
    assert url_join("example.com", "path", "to", "resource") == "example.com/path/to/resource"

  def test_joins_paths_with_leading_slash(self):
    assert url_join("example.com", "/path", "to", "resource") == "example.com/path/to/resource"

  def test_joins_paths_with_trailing_slash(self):
    assert url_join("example.com", "path", "to", "/resource") == "example.com/path/to/resource"

  def test_joins_full_uri(self):
    assert url_join("http://example.com", "path", "to", "resource") == "http://example.com/path/to/resource"

  def test_joins_with_empty_parts(self):
    assert url_join("example.com", "", "path", "", "resource") == "example.com/path/resource"

  def test_joins_with_multiple_slashes(self):
    assert url_join("example.com", "path//to", "resource") == "example.com/path/to/resource"