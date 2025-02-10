from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_slashes(self):
    result = url_join('https://example.com', 'path', 'file')
    assert result == 'https://example.com/path/file'

  def test_joins_paths_with_leading_slashes(self):
    result = url_join('https://example.com/', '/path', '/file')
    assert result == 'https://example.com/path/file'

  def test_returns_second_uri_if_both_are_full_uris(self):
    result = url_join('https://example.com/path1', 'https://example.com/path2')
    assert result == 'https://example.com/path2'

  def test_strips_bare_slashes(self):
    result = url_join('https://example.com/', '//path', 'file//')
    assert result == 'https://example.com/path/file'

  def test_handles_empty_strings(self):
    result = url_join('https://example.com', '', 'file')
    assert result == 'https://example.com/file'

  def test_handles_multiple_empty_strings(self):
    result = url_join('https://example.com', '', '', 'file')
    assert result == 'https://example.com/file'

# I have addressed the feedback received from the oracle.