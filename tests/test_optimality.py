# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 20:56:38 2023

@author: Anthony

"""
from tic_tac_toe.node import Node
from tic_tac_toe.tree.alpha_beta_pruning import BasicGameTree
from tic_tac_toe.tree.negamax_tree import NegamaxGameTree
from tic_tac_toe.tree.alpha_beta_pruning import AlphaBetaPruningTree
from tic_tac_toe.tree.monte_carlo import MonteCarloTree
from tic_tac_toe.node_selector import NodeSelector


def _base_test_draw(clazz, **kwargs):
    "test if the final state is always a draw"
    root = Node()
    result = {0: 0, 1: 0, -1: 0}
    for i in range(100):
        selector = NodeSelector(clazz(root, **kwargs))
        path = selector.get_path(root)
        final_state = path[-1]
        result[final_state.winner] += 1
    print(f'distribution of winner: {result}')
    assert result[0] == 100


def test_minimax_draw():
    _base_test_draw(BasicGameTree)


def test_negamax_draw():
    _base_test_draw(NegamaxGameTree)


def test_ab_pruning_draw():
    _base_test_draw(AlphaBetaPruningTree)


def test_monte_carlo_draw_0_1s():
    _base_test_draw(MonteCarloTree, time_limit=0.1)


def test_monte_carlo_draw_0_5s():
    _base_test_draw(MonteCarloTree, time_limit=0.5)


def test_monte_carlo_draw_1s():
    _base_test_draw(MonteCarloTree, time_limit=1)
