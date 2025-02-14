import os
from typing import List, Callable, Tuple
from src.utils.file_utils import load_tsplib, analyse_results
from src.ga.genetic_algorithm import GeneticAlgorithm
from src.ga.crossover import order_crossover, partially_mapped_crossover
from src.ga.mutation import inversion_mutation, relocation_mutation


def run_ga(
    dataset: str,
    curr_dir: str = "",
    population_sizes: List[int] = [200, 300, 400],
    crossover_rates: List[float] = [0.7, 0.8, 0.9],
    crossover_funcs: List[
        Callable[[List[int], List[int]], Tuple[List[int], List[int]]]
    ] = [order_crossover, partially_mapped_crossover],
    mutation_rates: List[float] = [0.05, 0.1, 0.2],
    mutation_funcs: List[Callable[[List[int]], None]] = [inversion_mutation, relocation_mutation],
    elitism_rate: float = 0.05,
    tournament_size: int = 3,
    generations: int = 4000,
    greedy_rate: float = 0.05,
    early_stop_threshold: int = 100
) -> None:
    """
    Runs a genetic algorithm on a dataset for various combinations of population sizes, crossover
    rates, mutation rates, and crossover and mutation functions.

    Args:
        dataset: The name of the dataset (should correspond to a `.tsp` file in `data/datasets`).
        curr_dir: The base directory where datasets and results are stored (default is "").
        population_sizes: A list of population sizes to test (default is [200, 300, 400]).
        crossover_rates: A list of crossover rates to test (default is [0.7, 0.8, 0.9]).
        crossover_funcs: A list of crossover functions to test (default is [order_crossover,
            partially_mapped_crossover]).
        mutation_rates: A list of mutation rates to test (default is [0.05, 0.1, 0.2]).
        mutation_funcs: A list of mutation functions to test (default is [inversion_mutation,
            relocation_mutation]).
        generations: The number of generations to run the algorithm for (default is 4000).
        elitism_rate: The proportion of individuals to retain through elitism (default is 0.05).
        tournament_size: The size of the tournament for selection (default is 3).
        greedy_rate: The probability of initialising an individual with a greedy heuristic.
        early_stop_threshold: The number of generations without improvement before stopping (
            default is 100).
    """
    coords = load_tsplib(os.path.join(curr_dir, f"data/datasets/{dataset}.tsp"))

    for population_size in population_sizes:
        for crossover_rate in crossover_rates:
            for mutation_rate in mutation_rates:
                for crossover_func in crossover_funcs:
                    for mutation_func in mutation_funcs:
                        ga = GeneticAlgorithm(
                            coords,
                            population_size,
                            crossover_rate,
                            crossover_func,
                            mutation_rate,
                            mutation_func,
                            generations,
                            elitism_rate,
                            tournament_size,
                            greedy_rate,
                            early_stop_threshold
                        )
                        ga.run()

                        results_path = os.path.join(
                            curr_dir,
                            f"data/results/{dataset}/pop{population_size}_{crossover_rate}"
                            f"{crossover_func.__name__}_{mutation_rate}{mutation_func.__name__}"
                            ".json"
                        )
                        ga.save_results(results_path)


if __name__ == "__main__":
    run_ga("berlin52")
    analyse_results("data/results/berlin52", "berlin52")
