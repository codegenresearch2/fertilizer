from .helpers import SetupTeardown

from src.utils import url_join


class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_none(self):
    path = url_join("http://example.com", "test", "file")

    assert path == "http://example.com/test/file"

  def test_joins_paths_with_leading_slash(self):
    path = url_join("http://example.com", "/test", "file")

    assert path == "http://example.com/test/file"

  def test_joins_paths_with_trailing_slash(self):
    path = url_join("http://example.com/", "test", "file")

    assert path == "http://example.com/test/file"

  def test_joins_paths_with_empty_parts(self):
    path = url_join("http://example.com", "", "file")

    assert path == "http://example.com/file"

  def test_joins_paths_with_none_parts(self):
    path = url_join("http://example.com", None, "file")

    assert path == "http://example.com/file"