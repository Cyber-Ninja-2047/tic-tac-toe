# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:34:02 2023

@author: Anthony

class MonteCarloTree

"""
import time
from math import inf
from random import choice
from queue import PriorityQueue
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


class MonteCarloTree(BasicGameTree):
    """
    The Minimax Game Tree with time limit.
    The non-terminal node will be scored by simulations.

    """

    renew = True

    _clazz_queue = PriorityQueue  # select the most promising node

    def __init__(self, root=None, depth_limit=None, time_limit=2,
                 exploration_weight=0):
        self.time_limit = time_limit
        self.exploration_weight = exploration_weight
        super().__init__(root=root, depth_limit=depth_limit)

    def _put(self, node):
        "put the given node into frontiers after checking node.depth"
        if self.depth_limit:
            if node.depth > self.depth_limit + self.root.depth:
                return

        self._frontiers.put((-self._get_priority(node), node))

    def _score_all(self):
        "Monte Carlo Tree will score nodes while expanding"
        return

    def _expand_all(self):
        start = time.time()
        while (not self._frontiers.empty()
               and time.time() - start < self.time_limit):
            self._expand_next()

    def _expand_next(self):
        _, node = self._frontiers.get()
        self._expand_the_node(node)
        for child in node.children:
            self._score(child)

    def _score(self, node):
        winner, _ = simulate(node)
        self._backpropagate(node, winner)

    def _backpropagate(self, node, winner):
        # update whole branch
        while node:
            win_total = self.get_simulations(node)

            # number of rollouts
            win_total[1] += 1

            # number of win
            win_total[0] += int(winner == node.turn)

            if node == self.root:
                break
            node = node.parent

    def _get_priority(self, node):
        exploitation = self.get_score(node)
        if (not self.exploration_weight
            or node == self.root
                or not node.parent):
            return exploitation

        node_rollouts = self.get_simulations(node)[1]
        parent_rollouts = self.get_simulations(node.parent)[1]
        exploration = self.exploration_weight * (node_rollouts /
                                                 (1 + parent_rollouts))**0.5
        return exploitation + exploration

    def get_score(self, node):
        "return the win ratio of the node, will be negative for MIN player"
        win_total = self.get_simulations(node)
        try:
            return win_total[0] / win_total[1] * node.turn
        except ZeroDivisionError:
            return 0

    def get_simulations(self, node):
        """
        return the simulations result of the node,

        returns
        -------
        win_total : [int, int],
            [win times, rollout times] for the node's player.

        """
        try:
            win_total = self.scores[node]
        except KeyError:
            win_total = [0, 0]
            self.scores[node] = win_total
        return win_total

    def _get_distribution(self, layer):
        distribution = {0: 0, 1: 0, -1: 0, -inf: 0, inf: 0}
        for node in layer:
            score = self.get_score(node)
            if score > 0:
                score = 1
            elif score < 0:
                score = -1
            distribution[score] += 1
        return distribution


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
        Node(),
        # Node([[1, 1, 0], [-1, -1, 0], [0, 0, 0]], turn=1),
        # Node([[1, 1, 0], [-1, -1, 0], [0, 0, -1]], turn=-1),
    ]

    for node in node_ls:
        tree = MonteCarloTree(root=node)
        print(f'{node}turn: {node.turn}')
        tree.show()
