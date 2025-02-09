from .helpers import SetupTeardown

from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_with_leading_slashes(self):
    result = url_join('/tmp', '/test', '/file')
    assert result == '/tmp/test/file'

  def test_joins_paths_with_none_values(self):
    result = url_join(None, 'test', None)
    assert result == 'test'

  def test_joins_full_uri(self):
    result = url_join('http://example.com', 'path', 'to', 'resource')
    assert result == 'http://example.com/path/to/resource'

  def test_strips_bare_slashes(self):
    result = url_join('/tmp', '/test/', '/file/')
    assert result == '/tmp/test/file'

  def test_handles_leading_and_trailing_slashes(self):
    result = url_join('/tmp/', 'test/', 'file/')
    assert result == '/tmp/test/file'