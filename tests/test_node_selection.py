# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 20:56:38 2023

@author: Anthony

test cases for node selection

"""
from tic_tac_toe.node import Node
from tic_tac_toe.tree.alpha_beta_pruning import BasicGameTree
from tic_tac_toe.tree.negamax_tree import NegamaxGameTree
from tic_tac_toe.tree.alpha_beta_pruning import AlphaBetaPruningTree
from tic_tac_toe.node_selector import NodeSelector


def _base_test_result(clazz):
    "test if the final state is always a draw"
    root = Node()
    tree = clazz(root)
    selector = NodeSelector(tree)

    # test the final result
    result = []
    for i in range(100):
        path = selector.get_path(root)
        final_state = path[-1]
        result.append(final_state.winner)

    # it should always be draw
    assert not any(result)


def test_minimax():
    _base_test_result(BasicGameTree)


def test_negamax():
    _base_test_result(NegamaxGameTree)


def test_ab_pruning():
    _base_test_result(AlphaBetaPruningTree)
