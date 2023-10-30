# Basic Policies

## Work Division

### ZHOU Huisheng (Anthony)

1. coding: implement the basic component Node on the game tree
2. coding: implement the alpha-beta pruning

### Khan Rovaid

1. coding: implement the basie component GameTree (minimax search algorithm)
2. coding: implement Monte Carlo tree search algorithm

### ABEEKPENG Paul Walier

1. coding: implement the CMD interface for a human player
2. testing: write unit tests
3. writing: write the progress report

### TAO Shiu Hei (Sharon)

1. testing: write unit tests
2. testing: analyze the improvement of alpha-beta pruning
4. writing: write the final report

## Install Project

We use **[poetry](https://python-poetry.org/docs/)** to manage this python project, please install poetry first.

Then, run `poetry install` in the root directory of this project to install this tic-tac-toe project. Poetry will create a virtual python environment automatically, you can choose to link this environment to you IDE (VS code, Spyder, etc.) or use your own environment by running `poetry config virtualenvs.create false` .

## Third-party Library

We are required finish this project without third-party library. Please don't import any external library except of the testing part.

## GitHub Flow

Create a branch for every change. And merge the branch to the main after the changes are complete. 

For more information, please refer [here](https://docs.github.com/en/get-started/quickstart/github-flow).

## Development Log

Please update the **[DEVLOG.md](./DEVLOG.md)** file descending by date once you reached a milestone (merge something to the main), to make reporting easier for our teammate.

## Naming Conventions

* package and module names: all-lowercase
* class names: CapitalWords
* function and variable names: all_lower_case
* constants: ALL_CAPITAL_LETTERS

For more information, please refer [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/#prescriptive-naming-conventions)

# Work Divide

## Basic Game Tree

Including 2 parts: the Node and the Game Tree. 

* **Node**: the atomic element of the Game Tree, storing attributes of the given state, including board status, parent node and child nodes. 
* **Game Tree**: the basic game tree, to expand nodes by depth first and calculate scores from the leaves to the root.

We can randomly select nodes with the same priority to make the game more various.

## A-B Pruning

We will create a class: Game Tree With AB Pruning inheriting the basic Game Tree class. And we can implement the A-B Pruning by just editing the expanding and scoring rule.

## Human Player

There are 2 possible implements about the human player.

1. we construct the entire tree when initialize the game, and match the node in the tree after the human moves. Then select the best move for the opposite. Loop until the game terminated. (Suitable for the basic Game Tree)
2. we build a new tree starting from the current board after every move from the human player. (Suitable for the Game Tree With AB Pruning because the tree does not contain all states)

We can just create a command-line version of the game. Below are some features need to be implemented:

1. allow the human choose to be player 1 (X) or player -1 (O).

2. input the coordinate to place a piece, e.g.
   ```
   # current board
     O X
   X   O
        
   # input
   (1, 1)
   
   # next board
     O X
   X X O
        
   ```

3. allow restart after game ends.

4. show the win-lose-draw situation.

## Testing

Testing including two parts below:

1. Write some unit test cases with **[pytest](https://docs.pytest.org/en/7.1.x/getting-started.html)**.
2. Run the game several times and make sure it is always a draw when computer vs computer and the computer never loses in the games with humans.
