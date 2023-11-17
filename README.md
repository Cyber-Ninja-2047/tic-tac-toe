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

We have a Command Line Interface for a human player.
After installing this project (`poetry install`), you can run command below to play the game.

```
>>> tic_tac_toe
Which side do you want to play (X/O)?
>>> X
Your next move is (row,column)?
>>> 1,1
--Your Move-----

  X

-----------------
--Computer Move--

  X
O
-----------------
# ......
--Computer Move--
O O
X X O
O X X
-----------------
Your next move is (row,column)?
>>> 0,2
--Your Move-----
O O X
X X O
O X X
-----------------
It's a draw!
Win: 0 Draw: 1 Lose: 0
Play again ([Y]/N)?
>>> N
```

You can also call the play function in Python to play this game.

```python
from tic_tac_toe.play import play
play()
```

## Show Results

You can print the game path through different algorithm.

### Minimax

```python
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
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

### Negamax

```python
from tic_tac_toe.tree.negamax_tree import NegamaxGameTree
from tic_tac_toe.node_selector import NodeSelector

# game tree of Negamax
tree = NegamaxGameTree()
tree.show()

# initialize the node selector
selector = NodeSelector(tree)

# get the game path
path = selector.get_path(tree.root)

# show the game path
selector.print_path(path)
```

### Alpha-Beta Pruning

```python
from tic_tac_toe.tree.negamax_tree import AlphaBetaPruningTree
from tic_tac_toe.node_selector import NodeSelector

# game tree of Alpha-Beta Pruning
tree = AlphaBetaPruningTree()
tree.show()

# initialize the node selector
selector = NodeSelector(tree)

# get the game path
path = selector.get_path(tree.root)

# show the game path
selector.print_path(path)
```

### Monte Carlo Tree

TBC
