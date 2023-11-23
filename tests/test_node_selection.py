# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 22:08:03 2023

@author: Sharon

"""
from tic_tac_toe.node import Node
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
from tic_tac_toe.tree.negamax_tree import NegamaxGameTree
from tic_tac_toe.tree.alpha_beta_pruning import AlphaBetaPruningTree
from tic_tac_toe.tree.monte_carlo import MonteCarloTree
from tic_tac_toe.node_selector import NodeSelector


DATA_LS_MAX = [[[1, 1, 0], [-1, -1, 0], [0, 0, 0]],
               [[1, 0, 0], [-1, 0, 0], [1, 0, -1]],
               [[0, 0, 0], [1, 0, 1], [-1, 0, -1]]]


DATA_LS_MIN = [[[1, 1, 0], [-1, -1, 0], [0, 0, 1]],
               [[1, 0, 1], [-1, 0, -1], [1, 0, 0]],
               [[0, 1, 0], [1, 0, 1], [-1, 0, -1]]]


def _print_possible_paths(paths):
    paths_str = []
    for path in paths:
        paths_str.append('\n'.join([str(node) for node in path]))

    for number, path_str in enumerate(paths_str):
        print("path ", number)
        print(path_str)


# test the node selection of states with MAX advantageous
def _node_selection_max(clazz):
    for data in DATA_LS_MAX:
        root = Node(data=data, turn=1)
        possible_paths = set()
        for i in range(100):
            tree = clazz(root)
            selector = NodeSelector(tree)
            path = selector.get_path(root)
            possible_paths.add(tuple(path))
        _print_possible_paths(possible_paths)
        print('-' * 10)

        for path in possible_paths:
            node = path[-1]
            assert node.terminated == True
            assert node.winner == 1


# test the node selection of states with MIN advantageous
def _node_selection_min(clazz):
    for data in DATA_LS_MIN:
        root = Node(data=data, turn=-1)
        possible_paths = set()
        for i in range(100):
            tree = clazz(root)
            selector = NodeSelector(tree)
            path = selector.get_path(root)
            node = path[-1]
            possible_paths.add(tuple(path))
        _print_possible_paths(possible_paths)

        for path in possible_paths:
            node = path[-1]
            assert node.terminated == True
            assert node.winner == -1


def test_minimax_max():
    _node_selection_max(BasicGameTree)


def test_minimax_min():
    _node_selection_min(BasicGameTree)


def test_negamax_max():
    _node_selection_max(NegamaxGameTree)


def test_negamax_min():
    _node_selection_min(NegamaxGameTree)


def test_ab_pruning_max():
    _node_selection_max(AlphaBetaPruningTree)


def test_ab_pruning_min():
    _node_selection_min(AlphaBetaPruningTree)


def test_monte_carlo_max():
    _node_selection_max(MonteCarloTree)


def test_monte_carlo_min():
    _node_selection_min(MonteCarloTree)
