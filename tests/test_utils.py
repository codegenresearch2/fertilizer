from .helpers import SetupTeardown
from src.utils import url_join, flatten

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    result = url_join("example.com", "path", "to", "resource")
    assert result == "example.com/path/to/resource"

  def test_joins_paths_with_leading_slash(self):
    result = url_join("example.com", "/path", "to", "resource")
    assert result == "example.com/path/to/resource"

  def test_joins_paths_with_trailing_slash(self):
    result = url_join("example.com", "path", "to", "/resource")
    assert result == "example.com/path/to/resource"

  def test_joins_full_uri(self):
    result = url_join("http://example.com", "path", "to", "resource")
    assert result == "http://example.com/path/to/resource"

  def test_joins_with_empty_parts(self):
    result = url_join("example.com", "", "path", "", "resource")
    assert result == "example.com/path/resource"

  def test_joins_with_multiple_slashes(self):
    result = url_join("example.com", "path//to", "resource")
    assert result == "example.com/path/to/resource"