import pytest
import random
from src.ga.mutation import inversion_mutation, relocation_mutation


def test_inversion_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests the inversion mutation function by mocking `random.sample` to return predefined indices
    and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the `random.sample` function.
    """
    monkeypatch.setattr(random, "sample", lambda a, b: [2, 5])

    # Invert the subpath [2, 3, 4, 5]
    individual = [0, 1, 2, 3, 4, 5, 6]
    expected_individual = [0, 1, 5, 4, 3, 2, 6]
    inversion_mutation(individual)

    assert individual == expected_individual


def test_relocation_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Tests the relocation mutation function by mocking `random.randint` to return predefined indices
    and comparing the generated offspring with expected children.

    Args:
        monkeypatch: A pytest fixture used to mock the `random.randint` function.
    """
    def mock_randint(a: int, b: int) -> int:
        # For subpath_length (1 to len(individual))
        if a == 1 and b == len(individual):
            return 3

        # For start (0 to len(individual) - subpath_length)
        if a == 0 and b == len(individual) - 3:
            return 1

        # For insert_pos (0 to len(individual))
        if a == 0 and b == len(individual):
            return 0

        return random.randint(a, b)

    monkeypatch.setattr(random, "randint", mock_randint)

    # Relocate the subpath [1, 2, 3] to position 0
    individual = [0, 1, 2, 3, 4, 5, 6]
    expected_individual = [1, 2, 3, 0, 4, 5, 6]
    relocation_mutation(individual)

    assert individual == expected_individual
