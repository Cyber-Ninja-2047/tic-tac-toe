# from random import choice

# from montecarlo_node import MCTNode

# # ... (previous code for MCTNode class)

# class MonteCarloTreeSearch:
#     """
#     Monte Carlo Tree Search (MCTS) algorithm.

#     params
#     ------
#     root : MCTNode,
#         The root node of the MCTS tree.
#     exploration_weight : float,
#         The exploration weight for the UCT (Upper Confidence Bound for Trees) value.
#     iterations : int,
#         The number of iterations to run the MCTS algorithm.

#     """

#     def __init__(self, root, exploration_weight=1.41, iterations=1000):
#         self.root = root
#         self.exploration_weight = exploration_weight
#         self.iterations = iterations

#     def search(self):
#         "Run the MCTS algorithm and return the best move"
#         for _ in range(self.iterations):
#             node_to_expand = self.select_node_to_expand()
#             score = self.simulate(node_to_expand)
#             self.backpropagate(node_to_expand, score)

#         # Select the best move based on UCT values
#         best_move = self.best_child(self.root).data
#         return best_move

#     def select_node_to_expand(self):
#         "Select a node to expand based on UCT values"
#         node = self.root
#         while not node.terminated and node.expanded:
#             children = node.children
#             if all(child.visits for child in children):
#                 node = self.best_child(node)
#             else:
#                 return node.expand_one(choice([i for i, child in enumerate(children) if not child.visits]))

#         return node

#     def best_child(self, node):
#         "Select the best child based on UCT values"
#         children = node.children
#         if not children:
#             # No children, return the node itself
#             return node
#         return max(children, key=node.uct_value)


#     def simulate(self, node):
#         "Run a simulation (playout) from the given node and return the final score"
#         while not node.terminated:
#             node = node.expand_one(choice(list(node.coordinates[0])))
#         return node.winner

#     def backpropagate(self, node, score):
#         "Backpropagate the simulation result up to the root"
#         while node:
#             node.update(score)
#             node = node.parent


# if __name__ == "__main__":
#     # Sample usage

#     # Build MCTS tree from an empty board
#     mcts_tree = MonteCarloTreeSearch(MCTNode(), iterations=10000)


#     # Run the MCTS algorithm to find the best move
#     best_move = mcts_tree.search()

#     print("Best move:", best_move)




from random import choice

from montecarlo_node import MCTNode

class MonteCarloTreeSearch:
    """
    Monte Carlo Tree Search (MCTS) algorithm.

    params
    ------
    root : MCTNode,
        The root node of the MCTS tree.
    exploration_weight : float,
        The exploration weight for the UCT (Upper Confidence Bound for Trees) value.
    iterations : int,
        The number of iterations to run the MCTS algorithm.

    """

    def __init__(self, root, exploration_weight=1.41, iterations=5000):
        self.root = root
        self.exploration_weight = exploration_weight
        self.iterations = iterations

    def search(self):
        "Run the MCTS algorithm and return the best move"
        for iteration in range(self.iterations):
            print(f"Iteration {iteration + 1}/{self.iterations}")
            node_to_expand = self.select_node_to_expand()
            score = self.simulate(node_to_expand)
            self.backpropagate(node_to_expand, score)

        # Select the best move based on UCT values
        best_child = self.best_child(self.root)
        if best_child:
            best_move = best_child.data
            print("Best move:", best_move)
            return best_move
        else:
            print("No best move found.")
            return None

    def select_node_to_expand(self):
        "Select a node to expand based on UCT values"
        node = self.root
        while not node.terminated and node.expanded:
            children = node.children
            if all(child.visits for child in children):
                node = self.best_child(node)
            else:
                return node.expand_one(choice([i for i, child in enumerate(children) if not child.visits]))

        return node

    def best_child(self, node):
        "Select the best child based on UCT values"
        children = node.children
        if children:
            return max(children, key=node.uct_value)
        else:
            return None

    def simulate(self, node):
        "Run a simulation (playout) from the given node and return the final score"
        while not node.terminated:
            node = node.expand_one(choice(list(node.coordinates[0])))
        return node.winner

    def backpropagate(self, node, score):
        "Backpropagate the simulation result up to the root"
        while node:
            node.update(score)
            node = node.parent


if __name__ == "__main__":
    # Sample usage
    root = MCTNode()

    # Build MCTS tree from an empty board
    node = root
    while not node.terminated:
        print(f'{node}--------')
        mcts_tree = MonteCarloTreeSearch(node)
        # Run the MCTS algorithm to find the best move
        node = mcts_tree.search()
