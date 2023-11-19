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


def _base_test_draw(clazz):
    "test if the final state is always a draw"
    root = Node()
    tree = clazz(root)
    selector = NodeSelector(tree)

    # test the final result
    for i in range(100):
        path = selector.get_path(root)
        final_state = path[-1]

        # it should always be draw
        assert final_state.winner == 0


def test_minimax_draw():
    _base_test_draw(BasicGameTree)


def test_negamax_draw():
    _base_test_draw(NegamaxGameTree)


def test_ab_pruning_draw():
    _base_test_draw(AlphaBetaPruningTree)
