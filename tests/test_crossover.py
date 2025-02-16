import pytest
import random
from src.ga.crossover import order_crossover, partially_mapped_crossover


def test_order_crossover(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests the order crossover (OX) function by mocking `random.sample` to return predefined indices
    and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the `random.sample` function.
    """
    monkeypatch.setattr(random, "sample", lambda a, b: [2, 5])

    parent1 = [1, 5, 4, 7, 6, 3, 2, 8]
    parent2 = [6, 8, 3, 2, 7, 4, 1, 5]
    expected_child1 = [3, 2, 4, 7, 6, 1, 5, 8]
    expected_child2 = [4, 6, 3, 2, 7, 8, 1, 5]

    child1, child2 = order_crossover(parent1, parent2)
    assert child1 == expected_child1
    assert child2 == expected_child2


def test_partially_mapped_crossover(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests the partially mapped function (PMX) function by mocking `random.sample` to return
    predefined indices and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the `random.sample` function.
    """
    monkeypatch.setattr(random, "sample", lambda a, b: [2, 5])

    parent1 = [1, 5, 4, 7, 6, 3, 2, 8]
    parent2 = [6, 8, 3, 2, 7, 4, 1, 5]
    expected_child1 = [1, 5, 3, 2, 7, 4, 6, 8]
    expected_child2 = [2, 8, 4, 7, 6, 3, 1, 5]

    child1, child2 = partially_mapped_crossover(parent1, parent2)
    assert child1 == expected_child1
    assert child2 == expected_child2
