# from math import inf

# from alpha_beta_pruning_tree import AlphaBetaPruningGameTree

# class NegamaxGameTree(AlphaBetaPruningGameTree):
#     def __init__(self, root=None, depth_limit=None):
#         super().__init__(root, depth_limit)

#     def _score(self, node, alpha=-inf, beta=inf):
#         "score of the given node by negamax with alpha-beta pruning"
#         if node.terminated:
#             return node.winner

#         max_score = -inf
#         for child in node.children:
#             score = -self.get_score(child, -beta, -alpha)
#             max_score = max(max_score, score)
#             alpha = max(alpha, score)

#             if alpha >= beta:
#                 break

#         self.scores[node] = max_score
#         return max_score

#     def get_score(self, node, alpha=-inf, beta=inf):
#         "get score of the given node with negamax and alpha-beta pruning"
#         try:
#             return self.scores[node]
#         except KeyError:
#             # return the -inf, so we can ignore nodes without score during selecting
#             return self._score(node, alpha, beta)


# if __name__ == '__main__':
#     # sample usage

#     # build tree from the empty board by default
#     tree = NegamaxGameTree()

#     # show layers of the tree
#     tree.show()



from alpha_beta_pruning_tree import AlphaBetaPruningGameTree


class NegamaxGameTree(AlphaBetaPruningGameTree):
    def __init__(self, root=None, depth_limit=None):
        super().__init__(root, depth_limit)

    def _score(self, node, alpha=-float('inf'), beta=float('inf')):
        "Score the given node using the negamax algorithm"
        if node.terminated:
            return node.winner
        else:
            child_scores = [-self.get_score(child, -beta, -alpha) for child in node.children]
            return max(child_scores, default=0)

    def get_score(self, node, alpha=-float('inf'), beta=float('inf')):
        "Get the score of the given node using the negamax algorithm"
        try:
            return self.scores[node]
        except KeyError:
            # Return the -inf, so we can ignore nodes without a score during selecting
            return -self._score(node, -beta, -alpha)

if __name__ == '__main__':
    # Sample usage for NegamaxGameTree

    # Build tree from the empty board by default
    tree = NegamaxGameTree()

    # Show layers of the tree
    tree.show()

