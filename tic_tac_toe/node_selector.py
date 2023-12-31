# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:05:00 2023

@author: Anthony

The NodeSelector class

"""
from math import isinf
from random import choice


class NodeSelector:
    """
    A selector, choosing the next best node from some given nodes
    base on a given game tree.

    params
    ------
    tree : GameTree,
        A game tree, having a "get_score" method that returns the score of a given node.

    kwargs
    ------
    Those keyword parameters will be used when the selector building a new tree.

    """

    def __init__(self, tree):
        self.tree = tree

    @staticmethod
    def print_path(path):
        "print the path and the winner"
        winner = path[-1].winner
        str_to_print = [''] + list(map(str, path)) + [f'winner: {winner}']
        print(('-' * 6 + '\n').join(str_to_print))

    def get_path(self, node):
        """
        Return the path from the given node to a terminal state

        params
        ------
        node : Node,
            The root node of the path.

        returns
        -------
        path : list of Node,
            The best game path from the given node to a terminal state.

        """
        path = []
        while node:
            path.append(node)
            node = self.get_next_node(node)
        return path

    def get_next_node(self, node):
        """
        Return the next best move of the given node

        params
        ------
        node : Node,
            The current node

        returns
        -------
        next_node : Node or None,
            The next best move.
            None means the current node is a terminal state.

        """
        # build a new tree from the given node if the node is not on the tree
        if ((self.tree.renew and self.tree.root != node)
                or isinf(self.tree.get_score(node))):
            self.tree = self.tree.transfer(root=node)

        # get child nodes
        children = node.expand()
        if not children:
            return None

        # select the best score
        scores = [self.tree.get_score(x) * node.turn for x in children]
        score = max(scores)
        children = [c for c, s in zip(children, scores) if s == score]

        # randomly select the next node in the same highest/lowest score
        # to make the game more varied
        next_node = choice(children)
        return next_node


if __name__ == "__main__":
    # sample usage
    from tic_tac_toe.tree.basic_game_tree import BasicGameTree

    tree = BasicGameTree()
    selector = NodeSelector(tree)

    # get the game path
    path = selector.get_path(tree.root)

    # show the game path
    selector.print_path(path)
