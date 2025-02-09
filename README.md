# CT421 - Artificial Intelligence - Evolutionary Search

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
### Running the Experiments
The Jupyter notebook, `notebooks/main.ipynb`, contains the entrypoints for all experiments on the TSPLIB datasets: `berlin52`, `kroA100`, and `pr1002`.

### Linting
```sh
flake8 .
```

### Testing
```sh
pytest
```