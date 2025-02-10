from .helpers import SetupTeardown
from src.utils import flatten

class TestFlatten(SetupTeardown):
  def test_flattens_single_level_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_already_flat_list(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

  def test_flattens_nested_list(self):
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

  def test_handles_empty_list(self):
    assert flatten([]) == []

  def test_handles_non_list_input(self):
    assert flatten(1) == [1]

  def test_handles_none_input(self):
    assert flatten(None) == [None]