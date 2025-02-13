# CT421 - Artificial Intelligence - Evolutionary Search

A genetic algorithm implementation for solving the Travelling Salesman Problem (TSP).

## Student Details
Student Name: Conor McNamara
Student ID: 21378116

## Prerequisites
- Python 3.x

## Installation
Clone the repository and install the required dependencies:

```sh
git clone https://github.com/conorjmcnamara/ct421_ga.git

pip install -r requirements/base.txt
```

To install development dependencies (for linting and testing), run:

```sh
pip install -r requirements/dev.txt
```

## Usage
### Running the Program
The Jupyter notebook, `notebooks/main.ipynb`, contains the entrypoints for experiments on the following TSPLIB datasets: `berlin52`, `kroA100`, and `pr1002`.

Alternatively, run the main script:
```sh
python -m src.main 
```

#### Customising Parameters
To run the program with custom parameters, modify the `run_ga()` function call's arguments. For example, to experiment with different population sizes and mutation rates, update the function call like so:

```py
run_ga("berlin52", population_sizes=[500, 1000], mutation_rates=[0.3])
```

#### Customising Datasets
To test other datasets, add the `.tsp` file inside the `/data/datasets` directory and update the `dataset` argument of the `run_ga()` function.

### Linting
```sh
flake8 .
```

### Testing
```sh
pytest
```