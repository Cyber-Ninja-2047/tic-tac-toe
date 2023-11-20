# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:34:02 2023

@author: Anthony

class MonteCarloTree

"""
import time
from math import inf, log
from random import choice
from queue import PriorityQueue
from tic_tac_toe.node import Node
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
from tic_tac_toe.winning_detector import WinningDetector


class MonteCarloTree(BasicGameTree):
    """
    The Minimax Game Tree with time limit.
    The non-terminal node will be scored by simulations.

    """

    renew = True

    _clazz_queue = PriorityQueue  # select the most promising node

    def __init__(self, root=None, depth_limit=None, time_limit=2,
                 exploration_weight=1.41,
                 scores_record=None, child_parents=None):
        super().__init__(root=root, depth_limit=depth_limit)
        start = time.time()
        self.time_limit = time_limit
        self.exploration_weight = exploration_weight
        self.__create_winning_detector(root)
        self._child2parents = {}
        if scores_record:
            self.scores = scores_record
        if child_parents:
            self._child2parents = child_parents

        self._expand_all_mcts()
        self.building_time = time.time() - start

    def transfer(self, root):
        "create a new tree starting with the given root, and save the scores record"
        return type(self)(root=root,
                          depth_limit=self.depth_limit,
                          time_limit=self.time_limit,
                          exploration_weight=self.exploration_weight,
                          scores_record=self.scores,
                          child_parents=self._child2parents)

    def __create_winning_detector(self, root):
        size = len(root.data)
        length = root.length
        self._winning_detector = WinningDetector(size, length)

    def simulate(self, node):
        "perform one simulation for the node"
        # TODO: the MCTS doesn't perform well, maybe the problem is the simulation
        initial_depth = node.depth
        # evaluation = self._stop_early(node)
        # if evaluation:
        #     return evaluation, 0

        while not node.terminated:
            # randomly explore
            index = choice(list(node.coordinates.get(0, [])))
            node = node.expand_one(index)
        return node.winner, node.depth - initial_depth

    def _stop_early(self, node):
        "stop if the node has some winning pattern"
        node.expand()
        draw, win, lose = zip(*[self._winning_detector.detect(c)
                                for c in node.children])
        parent_turn = -node.turn
        if parent_turn < 0:
            if any(win):
                return 1
        else:
            if any(lose):
                return -1
        return 0

    def _put(self, node):
        "put the given node into frontiers after checking node.depth"
        if self.depth_limit:
            if node.depth > self.depth_limit + self.root.depth:
                return

        self._frontiers.put((self._get_priority(node), node))

    def _score_all(self):
        "Monte Carlo Tree will score nodes while expanding"
        return

    def _expand_all(self):
        "override the expanding process"
        return

    def _expand_all_mcts(self):
        start = time.time()
        while time.time() - start < self.time_limit:
            while (not self._frontiers.empty()
                   and time.time() - start < self.time_limit):
                self._expand_next()
            # if not self._put_more():
            #     break
            break

    def _expand_next(self):
        if self._frontiers.empty():
            return
        _, node = self._frontiers.get()
        self._expand_the_node(node, False)

        for child in node.children:
            self._score(node)
            self._put(child)
            self._get_parents(child).append(node)

    def _get_parents(self, node):
        try:
            parents = self._child2parents[node]
        except KeyError:
            parents = [node.parent]
            self._child2parents[node] = parents
        return parents

    def _put_more(self):
        "put more node to expand if there are still times"
        if len(self.layers) < 2:
            return False
        for node in self.layers[1]:
            self._put(node)
        return True

    def _score(self, node):
        winner, depth = self.simulate(node)
        self._backpropagate(node, winner)
        return depth != 0

    def _backpropagate(self, node, winner):
        depth = node.depth - self.root.depth
        if node not in self._get_layer(depth):
            return

        draw_win_lose = self.get_simulation_result(node)
        draw_win_lose[winner] += 1
        if node == self.root:
            return

        for parent in self._get_parents(node):
            self._backpropagate(parent, winner)

    def _get_priority(self, node):
        parent_turn = -node.turn
        draw_win_lose = self.get_simulation_result(node)
        draw, win, lose = draw_win_lose
        node_rollouts = sum(draw_win_lose)

        # compute exploitation
        try:
            # count_not_bad = draw + draw_win_lose[self.root.turn]
            # exploitation = count_not_bad / node_rollouts
            exploitation = draw_win_lose[parent_turn] / node_rollouts
        except ZeroDivisionError:
            return -inf

        if (not self.exploration_weight
                or node == self.root):
            return -exploitation

        # compute exploration
        layer = self._get_layer(node.depth - self.root.depth - 1)
        parent_rollouts = sum([sum(self.get_simulation_result(p))
                               for p in self._get_parents(node)
                               if p in layer])

        exploration = (self.exploration_weight *
                       (log(parent_rollouts) / node_rollouts)**0.5)

        return -(exploitation + exploration)

    def get_score(self, node):
        "return the simulations times"
        # return -node.turn * self.get_simulation_result(node)[-node.turn]
        return -node.turn * sum(self.get_simulation_result(node))

    def get_simulation_result(self, node):
        """
        return the simulations result of the node,

        returns
        -------
        draw_win_lose : [int, int, int],
            [draw times, MAX won times, MIN won times]

        """
        try:
            draw_win_lose = self.scores[node]
        except KeyError:
            draw_win_lose = [0, 0, 0]
            self.scores[node] = draw_win_lose
        return draw_win_lose

    def _get_distribution(self, layer):
        distribution = {0: 0, 1: 0, -1: 0, -inf: 0, inf: 0}
        for node in layer:
            draw, win, lose = self.get_simulation_result(node)
            try:
                score = (win - lose) / (draw + win + lose)
            except ZeroDivisionError:
                score = 0
            if abs(score) < 0.5:
                score = 0
            elif score > 0:
                score = 1
            else:  # score < 0
                score = -1
            distribution[score] += 1
        return distribution


if __name__ == '__main__':
    # sample usage

    # 2 non-terminated nodes
    node_ls = [
        Node(),
    ]

    for node in node_ls:
        tree = MonteCarloTree(root=node)
        print(f'{node}turn: {node.turn}')
        tree.show()
