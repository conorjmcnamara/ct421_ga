import random
from typing import List


def inversion_mutation(individual: List[int]) -> None:
    """
    Applies inversion mutation to an individual by reversing a randomly selected subpath.

    Args:
        individual: A list of city indicies representing an individual.

    Returns:
        None. The mutation is applied in-place.
    """
    start, end = sorted(random.sample(range(len(individual)), 2))
    individual[start:end+1] = reversed(individual[start:end+1])


def relocation_mutation(individual: List[int]) -> None:
    """
    Applies relocation mutation to an individual by relocating a randomly selected subpath to a new
    position.

    Args:
        individual: A list of city indicies representing an individual.

    Returns:
        None. The mutation is applied in-place.
    """
    subpath_length = random.randint(1, len(individual))
    start = random.randint(0, len(individual) - subpath_length)

    subpath = individual[start:start + subpath_length]
    del individual[start:start + subpath_length]

    insert_pos = random.randint(0, len(individual))
    individual[insert_pos:insert_pos] = subpath
