from alpha_beta_pruning_tree import AlphaBetaPruningGameTree
from basic_game_tree import BasicGameTree
from math import inf, isinf

class GameTreeExplorer:
    def __init__(self, tree):
        self.tree = tree

    def explore(self, node):
        if node.terminated:
            return self.tree.get_score(node)

        children = node.expand()

        if node.turn == 1:  # Maximizing player's turn
            best_score = -inf
            for child in children:
                score = self.explore(child)
                best_score = max(best_score, score)
        else:  # Minimizing player's turn
            best_score = inf
            for child in children:
                score = self.explore(child)
                best_score = min(best_score, score)

        return best_score

if __name__ == "__main__":
    # Example usage
    tree = AlphaBetaPruningGameTree()
    explorer = GameTreeExplorer(tree)
    root = tree.root

    best_score = explorer.explore(root)
    print(f"Best score: {best_score}")
