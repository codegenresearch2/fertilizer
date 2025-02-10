from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

# The user prefers to use a utility function for URL joining and maintain consistent error handling across requests.
# The user prefers to maintain code readability and simplicity while using url_join over sane_join for URLs.
# The user prefers consistent naming conventions for functions and the use of url_join for URL construction.
# Therefore, the code snippet is rewritten as follows:

class TestUrlJoin(SetupTeardown):
  def test_joins_urls(self):
    assert url_join("http://example.com", "path", "file") == "http://example.com/path/file"

  def test_joins_urls_when_some_have_leading_slash(self):
    assert url_join("http://example.com", "/path", "file") == "http://example.com/path/file"