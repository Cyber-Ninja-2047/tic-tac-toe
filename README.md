# Tic-Tac-Toe
An adversarial game tree of tic-tac-toe.

## Installation

### Install by repository

Run codes below in the project's root directory after installing [pypoetry](https://python-poetry.org/docs/).

```shell
# if you don't need poetry's virtual environment
poetry config virtualenvs.create false

# install the project to your current python environment
poetry install
```

### Install by PyPI

This project hasn't been published on PyPI.

## Play

We are developing a Command Line Interface for a human player.

## Show Results

You can print the game path through different algorithm.

### Minimax

```python
from tic_tac_toe.basic_game_tree import BasicGameTree
from tic_tac_toe.node_selector import NodeSelector

# game tree of Minimax
tree = BasicGameTree()
tree.show()

# initialize the node selector
selector = NodeSelector(tree)

# get the game path
path = selector.get_path(tree.root)

# show the game path
selector.print_path(path)
```

### Alpha-Beta Pruning

TBC

### Monte Carlo Tree

TBC
