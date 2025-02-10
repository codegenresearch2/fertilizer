from .helpers import SetupTeardown
from src.utils import flatten

class TestFlatten(SetupTeardown):
  def test_flattens_nested_list(self):
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

  def test_returns_single_element_list(self):
    assert flatten(6) == [6]

  def test_returns_empty_list_for_empty_input(self):
    assert flatten([]) == []

  def test_flattens_empty_nested_list(self):
    assert flatten([[], [[]], [1, 2, 3]]) == [1, 2, 3]

  def test_handles_non_list_elements(self):
    assert flatten([1, [2, "three"], 4]) == [1, 2, "three", 4]