from typing import List, Tuple


def euclidean_distance(city1: Tuple[float, float], city2: Tuple[float, float]) -> float:
    return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5


def compute_distance_matrix(coords: List[Tuple[float, float]]) -> List[List[float]]:
    num_cities = len(coords)
    distance_matrix = [[0.0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(coords[i], coords[j])
    return distance_matrix


def fitness(individual: List[int], distance_matrix: List[List[float]]) -> float:
    # Total tour distance
    total_distance = 0.0
    for i in range(len(individual)):
        city1 = individual[i]
        city2 = individual[(i + 1) % len(individual)]
        total_distance += distance_matrix[city1][city2]
    return total_distance
