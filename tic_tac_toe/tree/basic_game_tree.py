# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 22:58:49 2023

@author: Anthony

The Basic Game Tree Class

"""
import time
from math import inf, isinf
from queue import LifoQueue
from tic_tac_toe.node import Node


class BasicGameTree:
    """
    The basic game tree using Minimax algorithm,
    also the base class of other types of game tree.
    It will expand all the nodes from the given root to leaves,
    or stop when reach the depth limit. After that, it will score all expanded
    nodes from the bottom.

    params
    ------
    root : Node or None,
        The given root of the tree. None means to start from an empty board.
    depth_limit : int or None,
        The depth limit of the tree, should only use on Monte Carlo Tree.
        None means no depth limit.

    attributes
    ----------
    layers : list,
        A nested list to store nodes layer by layer.
    scores : dict,
        node(Node) - score(-1, 0 or 1)
        A dictionary to match nodes to scores.
    building_time : float,
        The building time of the tree, in seconds.

    """

    def __init__(self, root=None, depth_limit=None):
        start_time = time.time()
        if root is None:
            root = Node()
        self.root = root
        self.depth_limit = depth_limit
        self.layers = []
        self.scores = {}

        # The Game Tree using depth-first search
        self._frontiers = LifoQueue()
        self._put(self.root)

        # expand all nodes automatically
        self._expand_all()

        # score all nodes after expanding
        self._score_all()

        # record the building time
        self.building_time = time.time() - start_time

    def show(self):
        "print size of each layers"
        print(f'building time of the tree: {self.building_time:.2f}s')
        print("depth    size    score_distrubution")
        for depth, layer in enumerate(self.layers):
            size = len(layer)
            print(f'{depth:<8d} {size:<7d} {self.__get_distrubution(layer)}')

    def __get_distrubution(self, layer):
        distribution = {0: 0, 1: 0, -1: 0, -inf: 0, inf: 0}
        for node in layer:
            distribution[self.get_score(node)] += 1
        return distribution

    def _put(self, node):
        "put the given node into frontiers after checking node.depth"
        if self.depth_limit:
            if node.depth > self.depth_limit:
                return
        self._frontiers.put(node)

    def _expand_all(self):
        "expand all nodes from the root to the leaves and store nodes into layers"
        while not self._frontiers.empty():
            self._expand_next()

    def _expand_next(self):
        "expand the next node"
        node = self._frontiers.get()
        self._expand_the_node(node)

    def _expand_the_node(self, node):
        # record the node
        if len(self.layers) <= node.depth:
            layer = []
            self.layers.append(layer)
        else:
            layer = self.layers[node.depth]
        layer.append(node)

        # expand the node
        children = node.expand()

        # put children to frontiers
        for child in children:
            self._put(child)

    def _score_all(self):
        "score all nodes from the bottom"
        for layer in self.layers[::-1]:
            for node in layer:
                self._score(node)

    def _score(self, node):
        "score the given node by minimax"
        if node.terminated:
            score = node.winner
        else:
            child_scores = map(self.get_score, node.children)

            # select the maximum score in +1 turn and minimum score in -1 turn
            score = max(child_scores, key=lambda x: x * node.turn)
            if isinf(score):
                score *= -1

        self.scores[node] = score

    def get_score(self, node):
        "get score of the given node"
        try:
            return self.scores[node]
        except KeyError:
            # return the -inf, so we can ignore nodes without score during selecting
            return inf * node.turn


if __name__ == '__main__':
    # sample usage

    # build tree from the empty board by default
    tree = BasicGameTree()

    # show layers of the tree
    tree.show()
