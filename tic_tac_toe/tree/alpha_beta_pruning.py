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

        # Do not expand if parent's score converged
        beta_previous, alpha_previous = self.get_score_range(previous_node)
        if alpha_previous == beta_previous:
            return False

        # Check parent's parent
        old_node = previous_node.parent
        if not old_node:
            return True

        # Pruning
        beta_old, alpha_old = self.get_score_range(old_node)

        # Adjusted pruning conditions
        if old_node.turn > 0:
            return alpha_previous >= beta_old
        else:
            return beta_previous <= alpha_old

    def _update_branch_from_leaf(self, current_node):
        "Update scores of nodes on the whole branch"
        # Check if node is None
        if current_node is None:
            return

        node = current_node.parent

        # Stop until reaching the root
        while node:
            score_range = self.get_score_range(node)
            if not node.children:
                continue

            # Max player
            if node.turn > 0:
                child_scores = [self.get_score_range(child)[1] for child in node.children]
                # Beta
                try:
                    score_range[0] = max(filter(filter_inf, child_scores))
                except ValueError:
                    pass
                # Alpha
                score_range[1] = max(child_scores)

            # Min player
            else:
                child_scores = [self.get_score_range(child)[0] for child in node.children]
                # Beta
                score_range[0] = min(child_scores)
                # Alpha
                try:
                    score_range[1] = min(filter(filter_inf, child_scores))
                except ValueError:
                    pass

            # Update the next parent
            node = node.parent

    def _score(self, current_node):
        """
        Compute score for the node.
        And update scores for every node on the branch
        when reaching a terminal state.

        """
        if current_node.terminated:
            self.scores[current_node] = [current_node.winner, current_node.winner]
            self._update_branch_from_leaf(current_node)
            return self.scores[current_node]

        # Middle nodes
        self.scores[current_node] = self.get_score_range(current_node)
        return self.scores[current_node]

    def get_score_range(self, current_node):
        """
        Return the score range of the node.
        It will be [-inf, inf] if the node is not scored.
        """
        try:
            score_range = self.scores[current_node]
        except KeyError:
            # Default score range
            score_range = [-inf, inf]
        return score_range

    def get_score(self, current_node):
        "Return the score of the node"
        if current_node.terminated:
            return current_node.winner

        score_range = self.get_score_range(current_node)
        score = max(score_range, key=lambda x: x * current_node.turn)
        return score


if __name__ == '__main__':
    # sample usage

    # build tree from the empty board by default
    alpha_beta_tree = AlphaBetaPruningTree()

    # show layers of the tree
    alpha_beta_tree.show()
