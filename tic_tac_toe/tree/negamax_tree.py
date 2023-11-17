from math import isinf
from tic_tac_toe.tree.basic_game_tree import BasicGameTree


class NegamaxGameTree(BasicGameTree):
    """
    This NegamaxGameTree is inherited from BasicGameTree i.e Minimax.
    The only difference between Negamax and MiniMax is the calculation logic of the score.
    The tree for both of them will be same.
    Maybe we can see the difference in the execution time of both trees.

    """
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
