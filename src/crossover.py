import random
from typing import List, Tuple, Dict


def order_crossover(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    """
    Performs order crossover (OX) on two parent individuals to produce two children.

    In this process, a random subpath from each parent is transferred into the corresponding child,
    and the remaining positions in each child is filled with genes from the opposite parent while
    preserving the relative order of the remaining genes.

    Args:
        parent1: The first parent represented as a list of city indicies.
        parent2: The second parent represented as a list of city indicies.

    Returns:
        A tuple containing two child individuals.
    """
    n = len(parent1)
    child1 = [-1] * n
    child2 = [-1] * n

    # Choose two random cut points
    start, end = sorted(random.sample(range(n), 2))

    # Copy the {start, end} gene subpath from parent1 to child1 and from parent2 to child2
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    def fill_child_pos(child: List[int], parent: List[int]) -> None:
        curr_pos = end

        for i in range(end, end + n):
            gene = parent[i % n]

            if gene not in child[start:end]:
                # Place the gene into the child's next available position
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

    In this process, a random subpath from each parent is transferred into the opposite child, and
    the remaining positions in each child is filled with genes from the corresponding parent,
    except when those genes were part of the transferred subpath, in which case the mapping between
    swapped genes is repeatedly followed until a valid replacement is found.

    Args:
        parent1: The first parent represented as a list of city indicies.
        parent2: The second parent represented as a list of city indicies.

    Returns:
        A tuple containing two child individuals.
    """
    n = len(parent1)
    child1 = [-1] * n
    child2 = [-1] * n

    # Choose two random cut points
    start, end = sorted(random.sample(range(n), 2))

    # Copy the {start, end} gene subpath from parent2 to child1 and from parent1 to child2
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
                    continue
                else:
                    # Handle conflicts
                    while gene in child:
                        gene = mapping[gene]
                    child[i] = gene

    fill_child_pos(child1, parent1, mapping2)
    fill_child_pos(child2, parent2, mapping1)
    return child1, child2
