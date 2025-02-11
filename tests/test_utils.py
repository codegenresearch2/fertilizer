from .helpers import SetupTeardown

from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_without_leading_slashes(self):
    result = url_join('api', 'v1', 'users')
    assert result == 'api/v1/users'

  def test_joins_paths_with_leading_slash_in_first_component(self):
    result = url_join('/api', 'v1', 'users')
    assert result == '/api/v1/users'

  def test_joins_paths_with_leading_slash_in_subsequent_components(self):
    result = url_join('api', '/v1', '/users')
    assert result == 'api/v1/users'

  def test_joins_full_uri(self):
    result = url_join('https://api.example.com', 'v1', 'users')
    assert result == 'https://api.example.com/v1/users'

  def test_joins_full_uri_with_leading_slash_in_subsequent_components(self):
    result = url_join('https://api.example.com', '/v1', '/users')
    assert result == 'https://api.example.com/v1/users'

  def test_handles_empty_strings(self):
    result = url_join('', 'v1', 'users')
    assert result == 'v1/users'

  def test_handles_empty_strings_with_leading_slash_in_subsequent_components(self):
    result = url_join('', '/v1', '/users')
    assert result == '/v1/users'

  def test_handles_leading_and_trailing_slashes(self):
    result = url_join('/api/', 'v1/', '/users/')
    assert result == '/api/v1/users/'