from math import inf
from basic_game_tree import BasicGameTree
from node import Node

class AlphaBetaPruningGameTree(BasicGameTree):
    def __init__(self, root=None, depth_limit=None):
        super().__init__(root, depth_limit)

    def _score(self, node, alpha=-inf, beta=inf):
        "score the given node by alpha-beta pruning"
        if node.terminated:
            score = node.winner
        else:
            child_scores = [self.get_score(child, alpha, beta) for child in node.children]

            if node.turn == 1:  # maximizing player
                score = max(child_scores)
                alpha = max(alpha, score)
            else:  # minimizing player
                score = min(child_scores)
                beta = min(beta, score)

        self.scores[node] = score
        return score

    def get_score(self, node, alpha=-inf, beta=inf):
        "get score of the given node with alpha-beta pruning"
        try:
            return self.scores[node]
        except KeyError:
            # return the -inf, so we can ignore nodes without score during selecting
            return self._score(node, alpha, beta)


if __name__ == '__main__':
    # sample usage

    # build tree from the empty board by default
    tree = AlphaBetaPruningGameTree()

    # show layers of the tree
    tree.show()
