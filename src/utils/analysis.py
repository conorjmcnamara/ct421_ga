import json
import os
import re
import matplotlib.pyplot as plt
import pandas as pd


def analyse_results(results_dir: str, dataset: str, skip: int = 0) -> None:
    """
    Analyzes the results of the genetic algorithm. This function aggreagtes results to a CSV file,
    finds the best configuration, and plots the fitness over generations.

    Args:
        results_dir: The directory containing results JSON files.
        dataset: The name of the dataset.
        skip: The number of initial generations to skip in the average fitness plot (default: 0).
    """
    aggregated_path = os.path.join(results_dir, "aggregated.csv")
    aggregate_results(aggregated_path, results_dir)

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

    plot_parameters(aggregated_path, dataset, "best_distance")
    plot_parameters(aggregated_path, dataset, "time")


def aggregate_results(aggregated_path: str, results_dir: str) -> None:
    """
    Aggregates results to a CSV file.

    Args:
        aggregated_path: The path to the aggregated results CSV file.
        results_dir: The directory containing results JSON files.
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

            data.append({
                "population": population,
                "crossover_rate": crossover_rate,
                "crossover_func": crossover_func,
                "mutation_rate": mutation_rate,
                "mutation_func": mutation_func,
                "time": time,
                "best_distance": best_distance
            })

    df = pd.DataFrame(data)
    df.to_csv(aggregated_path, index=False)
    print(f"Saved aggregated results to {aggregated_path}")


def plot_fitness(results_path: str, dataset: str, skip: int = 0) -> None:
    """
    Plots the fitness scores (average and best) per generation from a results file.

    Args:
        results_path: The path to the results JSON file.
        dataset: The name of the dataset.
        skip: The number of initial generations to skip in the average fitness plot (default: 0).
    """
    with open(results_path, "r") as file:
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
    plt.savefig(best_plot_path, bbox_inches="tight")
    plt.show()


def plot_parameters(
    aggregated_path: str,
    dataset: str,
    y_axis: str,
    sort_by: str = "best_distance",
    N: int = 10
) -> None:
    """
    Plots scatter plots with density color-coded circles for different parameters vs a user-defined
    metric.

    Args:
        aggregated_path: The path to the aggregated results CSV file.
        dataset: The name of the dataset.
        y_axis: The parameter to plot on the y-axis.
        sort_by: The parameter used to sort the top N results (default: 'best_distance').
        N: The number of top results to consider (default: 10).
    """
    data = pd.read_csv(aggregated_path)
    top_n_data = data.sort_values(by=sort_by).head(N)

    parameters = ["population", "crossover_rate", "mutation_rate"]

    for param in parameters:
        plt.figure(figsize=(10, 6))
        plt.scatter(
            top_n_data[param],
            top_n_data[y_axis],
            c=top_n_data[y_axis],
            cmap="coolwarm",
            s=400,
            alpha=0.7,
            edgecolors="k"
        )
        plt.colorbar(label="Value Intensity")
        plt.title(f"{dataset}: Top {N} by {sort_by} - {y_axis} vs {param}")
        plt.xlabel(param.replace("_", " ").title())
        plt.ylabel(y_axis.replace("_", " ").title())
        plt.tight_layout()

        file_name = f"{N}_{sort_by}_{y_axis}_{param}.png"
        plot_path = os.path.join(
            os.path.dirname(aggregated_path).replace("results", "plots"),
            file_name
        )
        plt.savefig(plot_path, bbox_inches="tight")
        plt.show()
