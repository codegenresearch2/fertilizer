from .helpers import SetupTeardown

from src.utils import flatten, url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

# No changes needed in this class as it doesn't violate any of the rules

The code snippet provided doesn't violate any of the rules, so there's no need to rewrite it. However, it's good to note that the `url_join` function from the `utils` module could be used in other parts of the codebase for URL construction as per the user's preference.