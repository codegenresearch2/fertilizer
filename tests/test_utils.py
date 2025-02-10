from .helpers import SetupTeardown
from src.utils import flatten

class TestFlatten(SetupTeardown):
  def test_flattens_single_level_list(self):
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]

  def test_returns_same_list_if_already_flat(self):
    assert flatten([1, 2, 3]) == [1, 2, 3]

  def test_flattens_deeply_nested_list(self):
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

  def test_handles_non_list_elements(self):
    assert flatten([1, [2, "three"], 4]) == [1, 2, "three", 4]

  def test_returns_empty_list_for_empty_input(self):
    assert flatten([]) == []

  def test_flattens_empty_nested_list(self):
    assert flatten([[], [[]], [1, 2, 3]]) == [1, 2, 3]