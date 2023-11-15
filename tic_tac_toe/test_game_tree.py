
from alpha_beta_pruning_tree import AlphaBetaPruningGameTree
from basic_game_tree import BasicGameTree


def test_game_tree(tree_class, tree_name):
    print(f"\nTesting {tree_name}:\n{'=' * (10 + len(tree_name))}")
    tree = tree_class()
    tree.show()

if __name__ == '__main__':
    # Test BasicGameTree
    test_game_tree(BasicGameTree, "Minimax")

    # Test AlphaBetaPruningGameTree
    test_game_tree(AlphaBetaPruningGameTree, "Alpha-beta Pruning")
