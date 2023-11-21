# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 12:34:02 2023

@author: Anthony, Rovaid

class MonteCarloTree

"""
import time
from math import inf, log
from random import choice
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
from tic_tac_toe.winning_detector import WinningDetector


class MonteCarloTree(BasicGameTree):
    """
    The Minimax Game Tree with time limit.
    The non-terminal node will be scored by simulations.

    params
    ------
    root : Node or None,
        The given root of the tree. None means to start from an empty board.
    depth_limit : int or None,
        The depth limit of the tree, should only use on Monte Carlo Tree.
        None means no depth limit.
    time_limit : float,
        The time limit of tree building.
    exploration_weight : float,
        The weight to choose nodes with fewer simulations.

    attributes
    ----------
    layers : list,
        A nested list to store nodes layer by layer.
    scores : dict,
        node(Node) - draw_win_lose([int, int, int])
        A dictionary to match nodes to simulation result,
        The simulation result are the numbers of draw, MAX win and MIN win respective
    building_time : float,
        The building time of the tree, in seconds.
    count_simulation : int,
        The total simulation times.
    renew : bool,
        Requiring renew after selecting the next node or not.

    """

    renew = True

    def __init__(self, root=None, depth_limit=None, time_limit=0.5,
                 exploration_weight=1.41):
        super().__init__(root=root, depth_limit=depth_limit)
        start = time.time()
        self.time_limit = time_limit
        self.exploration_weight = exploration_weight
        self.__create_winning_detector(self.root)
        self.count_simulation = 0

        self._expand_all_mcts()
        self.building_time = time.time() - start

    def transfer(self, root):
        "return the tree from the given root"
        return type(self)(root=root,
                          depth_limit=self.depth_limit, time_limit=self.time_limit)

    def __create_winning_detector(self, root):
        "create the winning pattern detector for the game board"
        size = len(root.data)
        length = root.length
        self._winning_detector = WinningDetector(size, length)

    def simulate(self, node):
        "perform one simulation for the node"
        self.count_simulation += 1

        # detect some winning patterns
        winner, to_expand = self._stop_early(node)
        if winner:
            return winner, to_expand

        while not node.terminated:
            # randomly explore
            index = choice(list(node.coordinates.get(0, set())))
            node = node.expand_one(index)
        return node.winner, True

    def _stop_early(self, node):
        "stop simulation if the node has some winning pattern"
        draw, win, lose = self._winning_detector.detect(node)
        if self.root.turn < 0:
            if win:
                # dont expand if an extreme disadvantage detected
                return 1, False
            if lose:
                return -1, True
        else:
            if lose:
                # dont expand if an extreme disadvantage detected
                return -1, False
            if win:
                return 1, True
        return 0, True

    def _score(self, node):
        "score the node by simulation"
        winner, to_expand = self.simulate(node)
        self._backpropagate(node, winner)
        return to_expand

    def _backpropagate(self, node, winner):
        "update the result for nodes on the whole branch"
        self.get_simulation(node)[winner] += 1
        if node == self.root:
            return

        self._backpropagate(node.parent, winner)

    def select(self):
        "select the next node to expand from root, but not frontiers"
        node = self.root
        while node.children:
            node = min(node.children, key=self._get_priority)
        return node

    def _get_priority(self, node):
        "the priority of expanding"
        draw_win_lose = self.get_simulation(node)
        node_rollouts = sum(draw_win_lose)

        # compute exploitation
        try:
            exploitation = (draw_win_lose[-node.turn] +
                            0.5 * draw_win_lose[0]  # draw is better than lose
                            ) / node_rollouts
        except ZeroDivisionError:
            return -inf

        if (not self.exploration_weight
                or node == self.root):
            return -exploitation

        # compute exploration
        if not self.count_simulation or not node_rollouts:
            return -inf
        exploration = (self.exploration_weight *
                       (log(self.count_simulation) / node_rollouts)**0.5)

        return -(exploitation + exploration)

    def _score_all(self):
        "Monte Carlo Tree will score nodes while expanding"
        return

    def _expand_all(self):
        "override the expanding process"
        return

    def _expand_all_mcts(self):
        "expand the tree if there is still time"
        # start from an unexpanded root
        self.root.clear_children()

        # expand if there is time
        start = time.time()
        while time.time() - start < self.time_limit:
            self._expand_next()

    def _expand_next(self):
        "select an node to expand"
        node = self.select()
        to_expand = self._score(node)
        self._expand_the_node(node, to_expand)

    def _expand_the_node(self, node, to_expand=False):
        "expand the node and put it into the correct layer"
        # record the node
        depth = node.depth - self.root.depth
        layer = self._get_layer(depth)
        layer.add(node)

        # expand the node
        if to_expand or node == self.root:  # the root should always be expanded
            node.expand()

    def _get_layer(self, depth):
        if len(self.layers) <= depth:
            layer = set()
            self.layers.append(layer)
        else:
            layer = self.layers[depth]
        return layer

    def get_simulation(self, node):
        "return the simulation result of the node"
        try:
            draw_win_lose = self.scores[node]
        except KeyError:
            draw_win_lose = [0, 0, 0]
            self.scores[node] = draw_win_lose
        return draw_win_lose

    def get_score(self, node):
        """
        return the simulation times times node.parent.turn.
        the node with most simulation times is the best move.

        """
        return -node.turn * sum(self.get_simulation(node))

    def _get_distribution(self, layer):
        distribution = {0: 0, 1: 0, -1: 0, -inf: 0, inf: 0}
        for node in layer:
            draw, win, lose = self.get_simulation(node)
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

    tree = MonteCarloTree()
    tree.show()
