from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

class TestUrlJoin(SetupTeardown):
  def test_joins_paths(self):
    assert url_join("/tmp", "test", "file") == "/tmp/test/file"

  def test_joins_paths_when_some_have_leading_slash(self):
    assert url_join("/tmp", "/test", "file") == "/tmp/test/file"

  def test_ignores_empty_strings(self):
    assert url_join("/tmp", "", "file") == "/tmp/file"

  def test_handles_single_argument(self):
    assert url_join("/tmp") == "/tmp"

In the updated code snippet, I have added a new test class `TestUrlJoin` that contains multiple test methods to cover various scenarios for the `url_join` function. I have also ensured consistent formatting and used descriptive test method names to improve readability and maintainability.