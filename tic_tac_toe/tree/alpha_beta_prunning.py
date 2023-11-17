# from math import inf
# from basic_game_tree import BasicGameTree

# class AlphaBetaPruningGameTree(BasicGameTree):
#     def __init__(self, root=None, depth_limit=None):
#         super().__init__(root, depth_limit)

#     def _score(self, node, alpha=-inf, beta=inf):
#         "score the given node by alpha-beta pruning"
#         if node.terminated:
#             score = node.winner
#         else:
#             child_scores = [self.get_score(child, alpha, beta) for child in node.children]

#             if node.turn == 1:  # maximizing player
#                 score = max(child_scores)
#                 alpha = max(alpha, score)
#             else:  # minimizing player
#                 score = min(child_scores)
#                 beta = min(beta, score)

#         self.scores[node] = score
#         return score

#     def get_score(self, node, alpha=-inf, beta=inf):
#         "get score of the given node with alpha-beta pruning"
#         try:
#             return self.scores[node]
#         except KeyError:
#             # return the -inf, so we can ignore nodes without score during selecting
#             return self._score(node, alpha, beta)


# if __name__ == '__main__':
#     # sample usage

#     # build tree from the empty board by default
#     tree = AlphaBetaPruningGameTree()

#     # show layers of the tree
#     tree.show()




from math import inf

from tic_tac_toe.tree.basic_game_tree import BasicGameTree

class AlphaBetaPruningGameTree(BasicGameTree):
    def __init__(self, root=None, depth_limit=None):
        super().__init__(root, depth_limit)

    def _put(self, node, alpha, beta):
        "Put the given node into frontiers after checking node.depth and alpha-beta scores"
        if self.depth_limit:
            if node.depth > self.depth_limit:
                return

        node_score = self.get_score(node, alpha, beta)
        if node_score > max(self.scores.values()):
            self._frontiers.put(node)

    def _expand_next(self, alpha, beta):
        "Expand the next node based on alpha-beta scores"
        node = self._frontiers.get()

        # Record the node
        if len(self.layers) <= node.depth:
            layer = []
            self.layers.append(layer)
        else:
            layer = self.layers[node.depth]
        layer.append(node)

        # Expand the node only if its score is promising
        node_score = self.get_score(node, alpha, beta)
        if node_score > max(self.scores.values()):
            children = node.expand()

            # Put children into frontiers
            for child in children:
                self._put(child, alpha, beta)

    def _score(self, node, alpha=-inf, beta=inf):
        "Score the given node by alpha-beta pruning"
        if node.terminated:
            score = node.winner
        else:
            # Prune if the score indicates this branch is not promising
            if node.turn == 1:  # maximizing player
                alpha = max(alpha, self.get_score(node, alpha, beta))
                if alpha >= beta:
                    self.scores[node] = alpha
                    return alpha

                child_scores = [self.get_score(child, alpha, beta) for child in node.children]
                score = max(child_scores)
                alpha = max(alpha, score)
            else:  # minimizing player
                beta = min(beta, self.get_score(node, alpha, beta))
                if alpha >= beta:
                    self.scores[node] = beta
                    return beta

                child_scores = [self.get_score(child, alpha, beta) for child in node.children]
                score = min(child_scores)
                beta = min(beta, score)

        self.scores[node] = score
        return score

if __name__ == '__main__':
    # Sample usage
    tree = AlphaBetaPruningGameTree()
    tree.show()
