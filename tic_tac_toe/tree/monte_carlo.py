# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:34:02 2023

@author: Anthony

class MonteCarloTree

"""
from math import inf
from random import choice
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


class MonteCarloTree(BasicGameTree):

    def __init__(self, root=None, depth_limit=4, n_iter=500, adjust_by_depth=False):
        self.n_iter = n_iter
        self.adjust_by_depth = adjust_by_depth
        super().__init__(root=root, depth_limit=depth_limit)

    def _score_all(self):
        "score all nodes from the bottom"
        # score all bottom nodes
        for node in self.layers[-1]:
            self.scores[node] = estimate_monte_carlo_score(
                node, self.n_iter, self.adjust_by_depth)

        # back propagate
        for layer in self.layers[-2::-1]:
            for node in layer:
                self._score(node)

    def __get_distribution(self, layer):
        distribution = {0: 0, 1: 0, -1: 0, -inf: 0, inf: 0}
        for node in layer:
            score = self.get_score(node)
            if score > 0:
                score = 1
            elif score < 0:
                score = -1
            distribution[score] += 1
        return distribution


def estimate_monte_carlo_score(node, n_iter=500, adjust_by_depth=False):
    """
    Use Monte Carlo Tree Search to estimate the score of the node

    params
    ------
    node : Node,
        the node to estimate.
    n_iter : int,
        simulation times.
    adjust_by_depth : bool,
        True means that shallower states will take more weight.

    returns
    -------
    score : float,
        the estimated score of the node.

    """
    if node.terminated:
        return node.winner

    # times of draw, max win, min win
    scores = [0, 0, 0]

    # perform simulations
    while n_iter > 0:
        winner, depth = simulate(node)
        if adjust_by_depth:
            depth = depth - node.depth
            scores[winner] += 1 / depth
        else:
            scores[winner] += 1

        n_iter -= 1

    # compute mct value
    try:
        score = (scores[1] / sum(scores[1:]) - 0.5) / 0.5
    # always draw
    except ZeroDivisionError:
        score = 0

    return score


def simulate(node):
    "perform one simulation"
    while not node.terminated:
        index = choice(list(node.coordinates.get(0, [])))
        node = node.expand_one(index)
    return node.winner, node.depth


if __name__ == '__main__':
    # sample usage

    from tic_tac_toe.node import Node

    # 2 non-terminated nodes
    node_ls = [
        Node([[1, 1, 0], [-1, -1, 0], [0, 0, 0]], turn=1),
        Node([[1, 1, 0], [-1, -1, 0], [0, 0, -1]], turn=-1),
    ]

    for node in node_ls:
        tree = MonteCarloTree(root=node)
        print(f'{node}turn: {node.turn}')
        tree.show()
