from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_trailing_slash(self):
    url = url_join("http://example.com", "path", "to", "resource")
    assert url == "http://example.com/path/to/resource"

  def test_joins_paths_with_trailing_slash(self):
    url = url_join("http://example.com/", "path", "to", "resource")
    assert url == "http://example.com/path/to/resource"

  def test_joins_paths_with_leading_slash(self):
    url = url_join("http://example.com", "/path", "to", "resource")
    assert url == "http://example.com/path/to/resource"

  def test_joins_paths_with_empty_parts(self):
    url = url_join("http://example.com", "", "path", "", "to", "resource")
    assert url == "http://example.com/path/to/resource"