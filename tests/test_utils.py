from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    result = url_join('http://example.com', 'path', 'file')
    assert result == 'http://example.com/path/file'

  def test_joins_paths_with_leading_slash(self):
    result = url_join('http://example.com', '/path', 'file')
    assert result == 'http://example.com/path/file'

  def test_replaces_path_with_full_uri(self):
    result = url_join('http://example.com/path1', 'http://example.com/path2')
    assert result == 'http://example.com/path2'

  def test_strips_bare_slashes(self):
    result = url_join('http://example.com/', '/path/', 'file')
    assert result == 'http://example.com/path/file'

  def test_handles_empty_strings(self):
    result = url_join('http://example.com', '', 'file')
    assert result == 'http://example.com/file'