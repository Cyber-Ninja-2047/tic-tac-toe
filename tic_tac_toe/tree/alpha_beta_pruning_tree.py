# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:02:12 2023

@author: f3420979
"""
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


class ABPruningTree(BasicGameTree):
    def _expand_all(self):
        "expand all nodes from the root to the leaves and store nodes into layers"
        while not self._frontiers.empty():
            self._expand_next()

    def _expand_next(self):
        "expand the next node"
        node = self._frontiers.get()

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
