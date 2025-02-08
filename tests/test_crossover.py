import random
from src.crossover import order_crossover, partially_mapped_crossover


def test_order_crossover(monkeypatch):
    """
    Tests the order crossover (OX) function by mocking `random.sample` to return predefined indices
    and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the random.sample function.
    """
    monkeypatch.setattr(random, "sample", lambda a, b: [3, 6])

    parent1 = [3, 4, 8, 2, 7, 1, 6, 5]
    parent2 = [4, 2, 5, 1, 6, 8, 3, 7]
    expected_child1 = [5, 6, 8, 2, 7, 1, 3, 4]
    expected_child2 = [4, 2, 7, 1, 6, 8, 5, 3]

    child1, child2 = order_crossover(parent1, parent2)
    assert child1 == expected_child1
    assert child2 == expected_child2


def test_partially_mapped_crossover(monkeypatch):
    """
    Tests the partially mapped function (PMX) function by mocking `random.sample` to return
    predefined indices and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the random.sample function.
    """
    monkeypatch.setattr(random, "sample", lambda a, b: [3, 6])

    parent1 = [3, 4, 8, 2, 7, 1, 6, 5]
    parent2 = [4, 2, 5, 1, 6, 8, 3, 7]
    expected_child1 = [3, 4, 2, 1, 6, 8, 7, 5]
    expected_child2 = [4, 8, 5, 2, 7, 1, 3, 6]

    child1, child2 = partially_mapped_crossover(parent1, parent2)
    assert child1 == expected_child1
    assert child2 == expected_child2
