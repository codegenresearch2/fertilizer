from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]


class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    assert url_join('/tmp', 'test', 'file') == '/tmp/test/file'

  def test_joins_paths_when_some_have_leading_slash(self):
    assert url_join('/tmp', '/test', 'file') == '/tmp/test/file'

  def test_joins_paths_with_multiple_slashes(self):
    assert url_join('/tmp', '/test/', '/file') == '/tmp/test/file'

  def test_joins_paths_with_trailing_slash(self):
    assert url_join('/tmp/', 'test/', 'file/') == '/tmp/test/file'

  def test_joins_paths_with_empty_strings(self):
    assert url_join('', 'test', '') == 'test'

  def test_joins_paths_with_none_values(self):
    assert url_join(None, 'test', None) == 'test'

  def test_joins_paths_with_mixed_types(self):
    assert url_join('/tmp', None, 'test', '', 'file') == '/tmp/test/file'
