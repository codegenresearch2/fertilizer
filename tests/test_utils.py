from .helpers import SetupTeardown
from src.utils import url_join

class TestUrlJoin(SetupTeardown):
  def test_joins_paths_correctly(self):
    test_cases = [
      ("https://example.com", "api", "users", "https://example.com/api/users"),
      ("https://example.com/", "api", "users", "https://example.com/api/users"),
      ("https://example.com", "/api", "users", "https://example.com/api/users"),
      ("https://example.com", "api/", "users", "https://example.com/api/users"),
      ("https://example.com", "", "api", "https://example.com/api"),
      ("https://example.com", "api", "", "https://example.com/api/"),
      ("https://example.com", "api", "users", "https://example.com/api/users"),
    ]

    for base, *parts, expected in test_cases:
      result = url_join(base, *parts)
      assert result == expected, f"Expected {expected}, but got {result}"