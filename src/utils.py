from .helpers import SetupTeardown
from src.utils import url_join

class TestFlatten(SetupTeardown):
  def test_flattens_list(self):
    assert url_join([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert url_join([1, 2, 3]) == [1, 2, 3]