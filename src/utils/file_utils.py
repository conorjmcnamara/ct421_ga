import json
import os
import re
import csv
import matplotlib.pyplot as plt
from typing import List, Tuple


def load_tsplib(path: str) -> List[Tuple[float, float]]:
    """
    Loads the coordinates of cities from a TSPLIB file.

    Args:
        path: The path to the TSPLIB file.

    Returns:
        A list of tuples representing the coordinates (x, y) of each city.
    """
    with open(path, 'r') as file:
        lines = file.readlines()
        node_coord_section = False
        coords = []

        for line in lines:
            if "NODE_COORD_SECTION" in line:
                node_coord_section = True
                continue
            if "EOF" in line:
                break
            if node_coord_section:
                parts = line.strip().split()
                coords.append((float(parts[1]), float(parts[2])))
        return coords


def analyse_results(results_dir: str, dataset: str, skip: int = 0) -> None:
    """
    Analyzes the results of the genetic algorithm. This function aggreagtes results to a CSV file,
    finds the best configuration, and plots the fitness over generations.

    Args:
        results_dir: The directory containing results JSON files.
        dataset: The name of the dataset.
        skip: The number of initial generations to skip in the average fitness plot (default: 0).
    """
    aggregate_results(results_dir)

    results_paths = [
        os.path.join(results_dir, filename)
        for filename in os.listdir(results_dir)
        if filename.endswith(".json")
    ]

    all_results = []
    for path in results_paths:
        with open(path, 'r') as file:
            data = json.load(file)
            all_results.append(data)

    if all_results:
        best_idx = min(range(len(all_results)), key=lambda i: all_results[i]["best_distance"])
        best_config = all_results[best_idx]
        best_path = results_paths[best_idx]

        print(f"Best configuration: {best_config}")
        plot_fitness(best_path, dataset, skip)


def aggregate_results(results_dir: str, output_csv: str = "aggregated.csv") -> None:
    """
    Aggregates results to a CSV file.

    Args:
        results_dir: The directory containing results JSON files.
        output_csv: The filename to the output CSV file.
    """
    data = []
    pattern = re.compile(r"pop(\d+)_([0-9.]+)(\w+)_([0-9.]+)(\w+)\.json")

    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            match = pattern.match(filename)
            if not match:
                continue

            population = int(match.group(1))
            crossover_rate = float(match.group(2))
            crossover_func = match.group(3)
            mutation_rate = float(match.group(4))
            mutation_func = match.group(5)

            file_path = os.path.join(results_dir, filename)
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)

            time = json_data.get("computational_secs", None)
            best_distance = json_data.get("best_distance", None)

            data.append([
                population, crossover_rate, crossover_func,
                mutation_rate, mutation_func, time, best_distance
            ])

    csv_path = os.path.join(results_dir, output_csv)
    with open(csv_path, 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "population",
            "crossover_rate",
            "crossover_func",
            "mutation_rate",
            "mutation_func",
            "time",
            "best_distance"
        ])
        writer.writerows(data)

    print(f"Saved aggregated results to {csv_path}")


def plot_fitness(results_path: str, dataset: str, skip: int = 0) -> None:
    """
    Plots the fitness scores (average and best) per generation from a results file.

    Args:
        results_path: The path to the results JSON file.
        dataset: The name of the dataset.
        skip: The number of initial generations to skip in the average fitness plot (default: 0).
    """
    with open(results_path, 'r') as file:
        results = json.load(file)

    avg_fitness = results["avg_fitness_per_gen"][skip:]
    best_fitness = results["best_fitness_per_gen"]
    generations = range(len(best_fitness))
    generations_skip = range(skip, len(best_fitness))

    # Plot average fitness
    plt.figure(figsize=(10, 6))
    plt.plot(generations_skip, avg_fitness, label="Average Fitness", color="blue", linewidth=2)
    plt.xlabel("Generations")
    plt.ylabel("Average Fitness")
    plt.title(f"{dataset}: Average Fitness vs Generations")
    plt.legend()
    plt.grid(True)

    avg_plot_path = results_path.replace("results", "plots").replace(".json", "_avg.png")
    os.makedirs(os.path.dirname(avg_plot_path), exist_ok=True)
    plt.savefig(avg_plot_path)
    plt.show()

    # Plot best fitness
    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_fitness, label="Best Fitness", color="red", linewidth=2)
    plt.xlabel("Generations")
    plt.ylabel("Best Fitness")
    plt.title(f"{dataset}: Best Fitness vs Generations")
    plt.legend()
    plt.grid(True)

    best_plot_path = results_path.replace("results", "plots").replace(".json", "_best.png")
    plt.savefig(best_plot_path)
    plt.show()
