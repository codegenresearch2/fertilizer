from .helpers import SetupTeardown

from src.utils import url_join


class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert url_join("https://example.com", "/api", "users") == "https://example.com/api/users"

  def test_returns_already_flat_list(self):
    assert url_join("https://example.com/api", "users") == "https://example.com/api/users"