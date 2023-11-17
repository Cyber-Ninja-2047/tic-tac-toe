# -- coding: utf-8 --
"""
Created on Wed Nov 15 16:16:26 2023

@author: Rovaid

The AlphaBetaPruningTree Class

"""
from math import isinf, inf
from basic_game_tree import BasicGameTree


def filter_inf(x):
    return not isinf(x)


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
        node = self._frontiers.get()

        # Score the node
        self._score(node)

        # Check the expanding
        if not self._check_expanding(node):
            return

        # Expand the node
        self._expand_the_node(node)

    def _check_expanding(self, node):
        """
        Check if expanding is needed.

        Returns
        -------
        to_expand_or_not : bool,
            True means to expand, False means to stop.

        """
        if node.terminated:
            return True

        parent = node.parent

        # Root node must be expanded
        if not parent:
            return True

        # Do not expand if parent's score converged
        beta_parent, alpha_parent = self.get_score_range(parent)
        if alpha_parent == beta_parent:
            return False

        # Check parent's parent
        grandparent = parent.parent
        if not grandparent:
            return True

        # Pruning
        beta_grand, alpha_grand = self.get_score_range(grandparent)

        # Adjusted pruning conditions
        if grandparent.turn > 0:
            return alpha_parent >= beta_grand
        else:
            return beta_parent <= alpha_grand

    def _update_branch_from_leaf(self, node):
        "Update scores of nodes on the whole branch"
        # Check if node is None
        if node is None:
            return

        node = node.parent

        # Stop until reaching the root
        while node:
            score_range = self.get_score_range(node)
            if not node.children:
                continue

            # Max player
            if node.turn > 0:
                child_scores = [self.get_score_range(c)[1] for c in node.children]
                # Beta
                try:
                    score_range[0] = max(filter(filter_inf, child_scores))
                except ValueError:
                    pass
                # Alpha
                score_range[1] = max(child_scores)

            # Min player
            else:
                child_scores = [self.get_score_range(c)[0] for c in node.children]
                # Beta
                score_range[0] = min(child_scores)
                # Alpha
                try:
                    score_range[1] = min(filter(filter_inf, child_scores))
                except ValueError:
                    pass

            # Update the next parent
            node = node.parent

    def _score(self, node):
        """
        Compute score for the node.
        And update scores for every node on the branch
        when reaching a terminal state.

        """
        if node.terminated:
            self.scores[node] = [node.winner, node.winner]
            self._update_branch_from_leaf(node)
            return self.scores[node]

        # Middle nodes
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
            # Default score range
            score_range = [-inf, inf]
        return score_range

    def get_score(self, node):
        "Return the score of the node"
        if node.terminated:
            return node.winner

        score_range = self.get_score_range(node)
        score = max(score_range, key=lambda x: x * node.turn)
        return score


if __name__ == '__main__':
    # sample usage

    # build tree from the empty board by default
    alpha_beta_tree = AlphaBetaPruningTree()

    # show layers of the tree
    alpha_beta_tree.show()
