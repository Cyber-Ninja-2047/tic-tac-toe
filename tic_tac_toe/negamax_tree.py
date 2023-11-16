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



from math import isinf
from alpha_beta_pruning_tree import AlphaBetaPruningGameTree
from basic_game_tree import BasicGameTree


class NegamaxGameTree(BasicGameTree):
    """THis NegamaxGameTree is inherited from BasicGameTree i.e Minimax.
    The only difference between Negamax and MiniMax is the calculation logic of the score
    The tree for both of them will be same.
    Maybe we can see the difference in the execution time of both trees."""
    def _score(self, node):
        "score the given node by negamax"
        if node.terminated:
            score = node.winner
        else:
            child_scores = map(self.get_score, node.children)

            # select the maximum score in +1 turn and minimum score in -1 turn
            score = node.turn * max([child*node.turn for child in child_scores])

        self.scores[node] = score

if __name__ == '__main__':
    # Sample usage for NegamaxGameTree

    # Build tree from the empty board by default
    tree = NegamaxGameTree()

    # Show layers of the tree
    tree.show()

