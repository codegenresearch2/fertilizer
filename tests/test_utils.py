from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_leading_or_trailing_slashes(self):
    path = url_join('api', 'v1', 'users')
    assert path == 'api/v1/users'

  def test_joins_paths_with_leading_slashes(self):
    path = url_join('/api', 'v1', 'users')
    assert path == '/api/v1/users'

  def test_joins_paths_with_trailing_slashes(self):
    path = url_join('api/', 'v1/', 'users')
    assert path == 'api/v1/users'

  def test_joins_paths_with_mixed_slashes(self):
    path = url_join('/api', 'v1/', 'users/')
    assert path == '/api/v1/users'

  def test_joins_full_uris(self):
    path = url_join('https://api.example.com', 'v1', 'users')
    assert path == 'https://api.example.com/v1/users'

  def test_joins_full_uris_with_leading_slashes(self):
    path = url_join('https://api.example.com/', 'v1', 'users')
    assert path == 'https://api.example.com/v1/users'

  def test_joins_full_uris_with_trailing_slashes(self):
    path = url_join('https://api.example.com/', 'v1/', 'users/')
    assert path == 'https://api.example.com/v1/users'

  def test_joins_full_uris_with_mixed_slashes(self):
    path = url_join('https://api.example.com/', 'v1/', 'users')
    assert path == 'https://api.example.com/v1/users'

  def test_handles_empty_strings(self):
    path = url_join('', 'v1', 'users')
    assert path == 'v1/users'

  def test_handles_empty_strings_with_leading_slashes(self):
    path = url_join('', '/v1', 'users')
    assert path == 'v1/users'

  def test_handles_empty_strings_with_trailing_slashes(self):
    path = url_join('', 'v1/', 'users')
    assert path == 'v1/users'

  def test_handles_empty_strings_with_mixed_slashes(self):
    path = url_join('', '/v1/', 'users/')
    assert path == 'v1/users'