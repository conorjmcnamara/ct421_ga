import random
from typing import List, Tuple, Dict


def order_crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Performs order crossover (OX) on two parent individuals to produce two children.

    - Select two random cut indices.
    - Copy the segment between the cut indices from each parent1 to child1.
    - Fill the remaining genes in child1 from parent2 in the same order, skipping duplicates,
    starting from the position just after where the copied segment ends.
    - Repeat for the second child using the opposite parent.

    Args:
        parent1: The first parent represented as a list of city indicies.
        parent2: The second parent represented as a list of city indicies.

    Returns:
        A tuple containing two child individuals.
    """
    n = len(parent1)
    child1 = [-1] * n
    child2 = [-1] * n

    start, end = sorted(random.sample(range(n), 2))

    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    def fill_child_pos(child: List[int], parent: List[int]) -> None:
        curr_pos = end

        for i in range(end, end + n):
            gene = parent[i % n]

            if gene not in child[start:end]:
                while child[curr_pos % n] != -1:
                    curr_pos += 1
                child[curr_pos % n] = gene

    fill_child_pos(child1, parent2)
    fill_child_pos(child2, parent1)
    return child1, child2


def partially_mapped_crossover(
    parent1: List[int],
    parent2: List[int]
) -> Tuple[List[int], List[int]]:
    """
    Performs partially mapped crossover (PMX) on two parents to produce two children.

    - Select two random cut indices.
    - Copy the segment between the cut indices from Parent 2 to Child 1.
    - Fill the remaining cities in Child 1 from Parent 1, handling conflicts with mappings:
        - If a city from Parent 1 has already been placed in Child 1 due to the copied segment from
        Parent 2, then use a mapping to find a city in Parent 1 that hasn't been used yet.
        - Look up the city in Parent 1 that corresponds to the conflicting city in Parent 2, and
        repeat this process until a city that hasn't been placed in Child 1 is found.
    - Repeat for the second child using the opposite parent.

    Args:
        parent1: The first parent represented as a list of city indicies.
        parent2: The second parent represented as a list of city indicies.

    Returns:
        A tuple containing two child individuals.
    """
    n = len(parent1)
    child1 = [-1] * n
    child2 = [-1] * n

    start, end = sorted(random.sample(range(n), 2))

    child1[start:end] = parent2[start:end]
    child2[start:end] = parent1[start:end]

    mapping1 = {parent1[i]: parent2[i] for i in range(start, end)}
    mapping2 = {parent2[i]: parent1[i] for i in range(start, end)}

    def fill_child_pos(child: List[int], parent: List[int], mapping: Dict[int, int]) -> None:
        for i in range(len(parent)):
            if child[i] == -1:
                gene = parent[i]
                if gene not in child[start:end]:
                    child[i] = gene
                else:
                    # Handle conflicts
                    while gene in child:
                        gene = mapping[gene]
                    child[i] = gene

    fill_child_pos(child1, parent1, mapping2)
    fill_child_pos(child2, parent2, mapping1)
    return child1, child2
