import random
from typing import List


def inversion_mutation(individual: List[int]) -> None:
    # Reverse a random subpath
    start, end = sorted(random.sample(range(len(individual)), 2))
    individual[start:end+1] = reversed(individual[start:end+1])


def relocation_mutation(individual: List[int]) -> None:
    # Relocate a random subpath
    subpath_length = random.randint(1, len(individual))
    start = random.randint(0, len(individual) - subpath_length)

    subpath = individual[start:start + subpath_length]
    del individual[start:start + subpath_length]

    insert_pos = random.randint(0, len(individual))
    individual[insert_pos:insert_pos] = subpath
