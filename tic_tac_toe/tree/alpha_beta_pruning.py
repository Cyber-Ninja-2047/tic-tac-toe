# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:16:26 2023

@author: Rovaid

The AlphaBetaPruningTree Class

"""
from math import isinf, inf
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


def _filter_converged_scores(score_range):
    return not any(map(isinf, score_range))


class AlphaBetaPruningTree(BasicGameTree):
    """
    Game tree implementation using Minimax algorithm with Alpha-Beta pruning.

    Parameters
    ----------
    root : Node or None,
        The root of the tree. None means starting from an empty board.
    depth_limit : int or None,
        The depth limit of the tree. None means no depth limit.

    Attributes
    ----------
    layers : list,
        A nested list to store nodes layer by layer.
    scores : dict,
        node(Node) - [minimum_score(-inf, -1, 0, or 1),
                      maximum_score(-1, 0, or 1, or inf)]
        A dictionary to match nodes to their score range.
    building_time : float,
        The building time of the tree, in seconds.

    """

    def _expand_next(self):
        "Expand the next node"
        current_node = self._frontiers.get()

        # Score the node
        self._score(current_node)

        # Check the expanding
        if not self._check_expanding(current_node):
            return

        # Expand the node
        self._expand_the_node(current_node)

    def _check_expanding(self, current_node):
        """
        Check if expanding is needed.

        Returns
        -------
        to_expand_or_not : bool,
            True means to expand, False means to stop.

        """
        if current_node.terminated:
            return True

        previous_node = current_node.parent

        # Root node must be expanded
        if not previous_node:
            return True

        # Do not expand if any previous node has converged score
        if self.__check_branch_converged(current_node):
            return False

        # Check parent's parent
        beta_previous, alpha_previous = self.get_score_range(previous_node)
        old_node = previous_node.parent
        if not old_node:
            return True

        # Pruning
        beta_old, alpha_old = self.get_score_range(old_node)

        # Adjusted pruning conditions
        if old_node.turn > 0:  # MAX player
            return alpha_previous >= beta_old
        # MIN player
        return beta_previous <= alpha_old

    def __check_branch_converged(self, node):
        node = node.parent
        while node:
            if _filter_converged_scores(self.get_score_range(node)):
                return True
            node = node.parent
        return False

    def _backpropagate(self, node):
        "Update the scores of nodes on the whole branch"
        node = node.parent

        # stop untill reach the root
        while node:
            score_range = self.get_score_range(node)
            child_scores = [self.get_score_range(c) for c in node.children]
            if not child_scores:
                continue
            converged_scores = filter(_filter_converged_scores, child_scores)

            # max player
            if node.turn > 0:
                child_alpha = [x[1] for x in child_scores]
                converged_alpha = [x[1] for x in converged_scores]

                # beta
                try:
                    score_range[0] = max(converged_alpha)
                except ValueError:
                    pass
                # alpha
                score_range[1] = max(child_alpha)

            # min player
            else:
                child_beta = [x[0] for x in child_scores]
                converged_beta = [x[0] for x in converged_scores]

                # beta
                score_range[0] = min(child_beta)
                # alpha
                try:
                    score_range[1] = min(converged_beta)
                except ValueError:
                    pass

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
            self._backpropagate(node)
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
        if _filter_converged_scores(score_range):
            score = max(score_range, key=lambda x: x * node.turn)
        else:
            score = node.turn * inf
        return score


def print_score_range(tree, node):
    "print score range for development"
    print(f'{node}score range: {tree.get_score_range(node)}\n---children---')
    for child in node.children:
        print(f'{child}score range: {tree.get_score_range(child)}')
    print('----------')


if __name__ == '__main__':
    # sample usage

    # build tree from the empty board by default
    alpha_beta_tree = AlphaBetaPruningTree()

    # show layers of the tree
    alpha_beta_tree.show()
