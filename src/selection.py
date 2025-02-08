import random
import copy
from typing import List


def elitism(
    population: List[List[int]],
    fitness_scores: List[float],
    elitism_count: int
) -> List[List[int]]:
    return [
        copy.deepcopy(population[i]) for i in sorted(
            range(len(fitness_scores)),
            key=lambda j: fitness_scores[j]
        )[:elitism_count]
    ]


def tournament_selection(
    population: List[List[int]],
    fitness_scores: List[float],
    tournament_size: int,
    elitism_count: int = 0
) -> List[List[int]]:
    selected = []
    for _ in range(len(population) - elitism_count):
        competitors = random.sample(list(zip(population, fitness_scores)), tournament_size)
        winner = min(competitors, key=lambda competitor: competitor[1])
        selected.append(winner[0])
    return selected
