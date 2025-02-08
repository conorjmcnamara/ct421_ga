import json
import os
import matplotlib.pyplot as plt
from typing import List, Tuple, Union, Dict


def load_tsplib(path: str) -> List[Tuple[float, float]]:
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


def read_results(path: str) -> Union[Dict, List]:
    with open(path, 'r') as file:
        return json.load(file)


def plot_fitness(results_path: str, dataset: str, skip: int = 0) -> None:
    results = read_results(results_path)

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
