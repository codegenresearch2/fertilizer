from .helpers import SetupTeardown
from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_single_level_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

  def test_flattens_nested_list(self):
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

  def test_handles_empty_list(self):
    assert flatten([]) == []

  def test_handles_non_list_input(self):
    assert flatten(1) == [1]

  def test_handles_none_input(self):
    assert flatten(None) == [None]

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_with_leading_slash(self):
    path = url_join("/tmp", "test", "file")
    assert path == "/tmp/test/file"

  def test_joins_paths_without_leading_slash(self):
    path = url_join("/tmp", "test", "file")
    assert path == "/tmp/test/file"

  def test_joins_paths_with_trailing_slash(self):
    path = url_join("/tmp", "test/", "file")
    assert path == "/tmp/test/file"

  def test_joins_full_urls(self):
    path = url_join("http://example.com", "test", "file")
    assert path == "http://example.com/test/file"

  def test_joins_full_urls_with_trailing_slash(self):
    path = url_join("http://example.com/", "test", "file")
    assert path == "http://example.com/test/file"

  def test_joins_full_urls_with_leading_slash(self):
    path = url_join("http://example.com/", "/test", "file")
    assert path == "http://example.com/test/file"

  def test_handles_empty_parts(self):
    path = url_join("http://example.com", "", "test", "")
    assert path == "http://example.com/test"

  def test_handles_only_slashes(self):
    path = url_join("http://example.com", "/", "/", "/")
    assert path == "http://example.com"