# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:16:26 2023

@author: Anthony

The AlphaBetaPruningTree Class

"""
from math import isinf, inf
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


def filter_inf(x):
    return not isinf(x)


class AlphaBetaPruningTree(BasicGameTree):
    """
    The game tree using Minimax algorithm with Alpha-Beta pruning.
    It will score nodes when expanding,
    and skip some branchs that make no effects to the result.

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
        node(Node) - [minimum_score(-inf, -1, 0 or 1),
                      maximum_score(-1, 0 or 1 or inf)]
        A dictionary to match nodes to their score range.
    building_time : float,
        The building time of the tree, in seconds.

    """

    def _expand_next(self):
        "expand the next node"
        node = self._frontiers.get()

        # score the node
        self._score(node)

        # check the expanding
        if not self._check_expanding(node):
            return

        # expand the node
        self._expand_the_node(node)

    def _check_expanding(self, node):
        """
        Check if the expanding is needed.

        returns
        -------
        to_expand_or_not : bool,
            True means to expand, False means to stop.

        """
        # the terminal state should be record
        if node.terminated:
            return True

        parent = node.parent

        # root node must be expanded
        if not parent:
            return True

        # do not expand if parent's score converged
        beta_parent, alpha_parent = self.get_score_range(parent)
        if alpha_parent == beta_parent:
            return False

        # check parent's parent
        grandparent = parent.parent
        if not grandparent:
            return True

        beta_grand, alpha_grand = self.get_score_range(grandparent)
        if grandparent.turn > 0:
            return alpha_parent >= beta_grand
        else:
            return beta_parent <= alpha_grand

        return True

    def _score_all(self):
        """
        Alpha-Beta pruning will score nodes when expanding
        so we don't need to score all nodes again

        """
        return

    def _update_branch_from_leaf(self, node):
        "Update the scores of nodes on the whole branch"
        node = node.parent

        # stop untill reach the root
        while node:
            score_range = self.get_score_range(node)
            if not node.children:
                continue

            # max player
            if node.turn > 0:
                child_scores = [self.get_score_range(c)[1]
                                for c in node.children]
                # beta
                score_range[0] = max(filter(filter_inf, child_scores))
                # alpha
                score_range[1] = max(child_scores)

            # min player
            else:
                child_scores = [self.get_score_range(c)[0]
                                for c in node.children]
                # beta
                score_range[0] = min(child_scores)
                # alpha
                score_range[1] = min(filter(filter_inf, child_scores))

            # update the next parent
            node = node.parent

    def _score(self, node):
        """
        Compute score for the node.
        And update scores for every nodes on the branch
        when reach a terminal state.

        """
        if node.terminated:
            self.scores[node] = [node.winner, node.winner]
            self._update_branch_from_leaf(node)
            return self.scores[node]

        # middle nodes
        self.scores[node] = self.get_score_range(node)
        return self.scores[node]

    def get_score_range(self, node):
        """
        Return the score range of the node.
        It will be [-inf, inf] if the node is not scored.
        """
        try:
            score_range = self.scores[node]
        except KeyError:
            # default score range
            score_range = [-inf, inf]
        return score_range

    def get_score(self, node):
        "Return the score of the node"
        if node.terminated:
            return node.winner

        score_range = self.get_score_range(node)
        score = max(score_range, key=lambda x: x * node.turn)
        return score