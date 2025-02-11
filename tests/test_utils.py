from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    assert url_join('api', 'v1', 'users') == 'api/v1/users'
    assert url_join('/api', 'v1', 'users') == '/api/v1/users'
    assert url_join('api/', 'v1/', 'users/') == 'api/v1/users/'
    assert url_join('/api', 'v1/', 'users/') == '/api/v1/users/'
    assert url_join('https://api.example.com', 'v1', 'users') == 'https://api.example.com/v1/users'
    assert url_join('https://api.example.com/', 'v1', 'users') == 'https://api.example.com/v1/users'
    assert url_join('https://api.example.com/', 'v1/', 'users/') == 'https://api.example.com/v1/users/'
    assert url_join('https://api.example.com/', 'v1/', 'users') == 'https://api.example.com/v1/users'
    assert url_join('', 'v1', 'users') == 'v1/users'
    assert url_join('', '/v1', 'users') == '/v1/users'
    assert url_join('', 'v1/', 'users') == 'v1/users'
    assert url_join('', '/v1/', 'users/') == '/v1/users/'