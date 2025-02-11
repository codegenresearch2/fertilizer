from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    result = url_join('http://example.com', 'path', 'file')
    assert result == 'http://example.com/path/file'

  def test_joins_paths_with_leading_slash(self):
    result = url_join('http://example.com', '/path', 'file')
    assert result == 'http://example.com/path/file'

  def test_joins_full_uris(self):
    result = url_join('http://example.com/', 'https://another.com/path')
    assert result == 'https://another.com/path'

  def test_strips_bare_slashes(self):
    result = url_join('http://example.com/', '/')
    assert result == 'http://example.com'

  def test_handles_empty_strings(self):
    result = url_join('http://example.com', '', 'file')
    assert result == 'http://example.com/file'

  def test_handles_trailing_slashes(self):
    result = url_join('http://example.com/', 'path/')
    assert result == 'http://example.com/path'

  def test_handles_leading_and_trailing_slashes(self):
    result = url_join('http://example.com/', '/path/')
    assert result == 'http://example.com/path'