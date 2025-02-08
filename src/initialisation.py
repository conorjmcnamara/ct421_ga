import random
from typing import List


def init_population(
    population_size: int,
    num_cities: int,
    distance_matrix: List[List[float]],
    random_rate: float
) -> List[List[int]]:
    population = []

    for _ in range(population_size):
        if random.random() < random_rate:
            individual = random.sample(range(num_cities), num_cities)
        else:
            individual = greedy_heuristic(num_cities, distance_matrix)

        population.append(individual)
    return population


def greedy_heuristic(num_cities: int, distance_matrix: List[List[float]]) -> List[int]:
    # Nearest neighbour
    cities = set(range(num_cities))
    start_city = random.choice(list(cities))
    path = [start_city]
    cities.remove(start_city)

    curr_city = start_city
    while cities:
        next_city = min(cities, key=lambda city: distance_matrix[curr_city][city])
        path.append(next_city)
        cities.remove(next_city)
        curr_city = next_city
    return path
