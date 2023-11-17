# 2023-10-18

Author: Anthony

Completed the class Node, including features below:

* storing important properties:
  1. board status
  2. current turn
  3. parent node
  4. child nodes
* when the node is instantiated, automatically determine whether the node is terminal state and the winner of the node.

* the "expand" method, to generate and return all child nodes.

The users only need to instantiate the Node once. Then access the properties "terminated" and "winner" to check the status, or call method "expand" to get nodes in the next layer instead of to calculate board status manually every time.

# 2023-11-03

Author: Anthony

Fixed the bug that Node.terminated remained True when the game board was fulled.

# 2023-11-04

Author: Anthony

Completed the class BasicGameTree, including features below:

* automatically expand all the nodes from the given root to leaves.
* automatically score all the nodes from the bottom using Minimax algorithm.
* the "get_score" method, returning the score of a given node.
* the "show" method, showing the distrubution of every layers and the tree building time.

Completed the class NodeSelector, including features below:

* compatible with any types of game tree that has a "get_score" method.
* the "get_next_node" method, returning the next best node from a given node base on the given game tree.
* the "get_path" method, returning the game path from the given root node.
* automatically build a new tree from the given node if the node is not on the original tree.

# 2023-11-09

Author: Paul

Implementing the CMD interface for a human player:

* The program imports necessary classes from the 'tic_tac_toe' package.
* The 'initialize_game' function sets up the game, creating a new game tree and a node selector.
* The 'choose_a_side' function allows the player to choose between 'X' or 'O', which are mapped to numeric values.
* The 'player_move' function lets the player make a move by inputting an index. It checks for valid input and whether the chosen cell is empty.
* The 'computer_move' function uses the 'NodeSelector' to determine and make the computer's move.
* The 'main_function' controls the game flow, alternating between player and computer moves until the game ends. It then prints the result and asks if the player wants to play again

If the script is run as a main script, it starts the game by calling the 'main_function'. This script allows a human player to play Tic-Tac-Toe against a computer, with the computer's moves determined by a simple adversarial search algorithm.

# 2023-11-16

Author: Anthony

Optimized the human player interface, including features below:

* record the win-draw-lose times.
* allow user to select another type of game tree.
* allow user to input upper or lower case.
* do not rebuild the tree in replaying, it saves much time when using the minimax game tree.
* give more hints if user's input is invalid.
* check the inputted index range.

Fixed a bug for NodeSelector when it building a new tree.

# 2023-11-17

Author: Rovaid

1. Alpha-Beta Pruning Implementation
* Alpha-Beta Pruning Tree (Class: AlphaBetaPruningTree)
Efficient Traversal: The AlphaBetaPruningTree class optimizes game tree traversal using the Alpha-Beta Pruning algorithm.
Dynamic Expansion: The tree dynamically expands based on the current game state, minimizing unnecessary node exploration.
Pruning Conditions: Alpha-beta pruning conditions efficiently eliminate branches that do not impact the final decision.
Score Maintenance: The _update_branch_from_leaf method ensures accurate score updates throughout the tree.
* Key Methods
* _expand_next()

Purpose: Expands the next node in the game tree.
Functionality: Scores the node, checks if expanding is needed based on pruning conditions, and expands the node if necessary.

* _check_expanding(current_node)
Purpose: Determines whether expanding the current node is needed.
Functionality: Checks termination status, ensures the root node is expanded, and implements pruning conditions based on alpha and beta values.
* _update_branch_from_leaf(current_node)

Purpose: Updates scores of nodes on the entire branch.
Functionality: Traverses from the leaf to the root, updating score ranges based on child nodes' scores.
* _score(current_node)
Purpose: Computes the score for the node.
Functionality: Handles terminal nodes by setting winner scores, updates scores for nodes on the branch when reaching a terminal state, and computes scores for middle nodes.
* get_score_range(current_node)
Purpose: Returns the score range of a given node.
Functionality: Retrieves the score range from the scores dictionary or defaults to [-inf, inf] if the node is not scored.
* get_score(current_node)
Purpose: Returns the score of the node.
Functionality: Considers terminal states and computes the score based on the maximum of the score range, considering the current node's turn. 
2. NegaMax Algorithm
  * It's inherited from the BasicGameTree class
  * The only difference between NegaMax and MiniMax is the scoring logic. which is minimax uses if ~ else statement for calculating the minimum and maximum player score and negamax uses the calculation logic which is score = turn*([score*turn for  score in child_scores])
