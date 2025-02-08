# CT421 - Artificial Intelligence - Evolutionary Search

## Installation
```sh
pip install -r requirements/base.txt

# Development dependencies (for linting and testing)
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