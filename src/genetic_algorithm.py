import time
import random
import copy
import os
import json
from typing import List, Tuple, Callable
from src.fitness import compute_distance_matrix, fitness
from src.initialisation import init_population
from src.selection import elitism, tournament_selection


class GeneticAlgorithm:
    def __init__(
        self,
        coords: List[Tuple[float, float]],
        population_size: int,
        crossover_rate: float,
        crossover_func: Callable[[List[int], List[int]], Tuple[List[int], List[int]]],
        mutation_rate: float,
        mutation_func: Callable[[List[int]], None],
        elitism_rate: float,
        tournament_size: int,
        generations: int,
        init_population_random_rate: float,
        early_stop_threshold: int
    ):
        self.crossover_rate = crossover_rate
        self.crossover_func = crossover_func
        self.mutation_rate = mutation_rate
        self.mutation_func = mutation_func

        self.elitism_count = int(elitism_rate * population_size)
        self.tournament_size = tournament_size
        self.generations = generations
        self.init_pop_random_rate = init_population_random_rate
        self.early_stop_threshold = early_stop_threshold

        self.distance_matrix = compute_distance_matrix(coords)
        self.population = init_population(
            population_size,
            len(coords),
            self.distance_matrix,
            init_population_random_rate
        )

        self.avg_fitness_per_gen = []
        self.best_fitness_per_gen = []
        self.best_distance = float("inf")
        self.best_solution = None
        self.no_improvement_count = 0
        self.computational_secs = None

    def run(self) -> None:
        start_time = time.time()

        for _ in range(self.generations):
            # Evaluate fitness
            fitness_scores = [
                fitness(individual, self.distance_matrix) for individual in self.population
            ]

            self.avg_fitness_per_gen.append(sum(fitness_scores) / len(fitness_scores))
            gen_best_fitness = min(fitness_scores)
            self.best_fitness_per_gen.append(gen_best_fitness)

            if gen_best_fitness < self.best_distance:
                self.best_distance = gen_best_fitness
                self.best_solution = copy.deepcopy(
                    self.population[fitness_scores.index(gen_best_fitness)]
                )
                self.no_improvement_count = 0
            else:
                self.no_improvement_count += 1

            # Check for early stopping
            if self.no_improvement_count >= self.early_stop_threshold:
                break

            # Elitism
            elite_individuals = elitism(self.population, fitness_scores, self.elitism_count)

            # Selection
            selected_population = tournament_selection(
                self.population,
                fitness_scores,
                self.tournament_size,
                self.elitism_count
            )

            # Crossover
            next_population = []
            for i in range(0, len(selected_population) - 1, 2):
                parent1, parent2 = selected_population[i], selected_population[i+1]

                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover_func(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                next_population.extend([child1, child2])

            # Handle odd-length populations
            if len(selected_population) % 2 == 1:
                next_population.append(selected_population[-1])

            # Mutation
            for i in range(len(next_population)):
                if random.random() < self.mutation_rate:
                    self.mutation_func(next_population[i])

            self.population = elite_individuals + next_population
        self.computational_secs = time.time() - start_time

    def save_results(self, path: str) -> None:
        results = {
            "computational_secs": round(self.computational_secs, 4),
            "best_distance": round(self.best_distance, 4),
            "best_solution": self.best_solution,
            "avg_fitness_per_gen": [round(fitness, 4) for fitness in self.avg_fitness_per_gen],
            "best_fitness_per_gen": [round(fitness, 4) for fitness in self.best_fitness_per_gen]
        }

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            json.dump(results, file, indent=4)
