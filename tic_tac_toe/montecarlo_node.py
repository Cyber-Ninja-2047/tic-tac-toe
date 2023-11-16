from copy import deepcopy
from itertools import product
from random import choice

from node import Node

def delta_filter(indices):
    "filtering the delta of indices"
    if len(indices) != 2:
        return False
    index_1, index_2 = indices
    return (index_1[0] + index_2[0] == 0 and
            index_1[1] + index_2[1] == 0)

INDICES_DELTA = list(product((-1, 0, 1), (-1, 0, 1)))
INDICES_PAIRS = set(filter(delta_filter, map(
    frozenset, product(INDICES_DELTA, INDICES_DELTA))))
LEN_TICTACTOE = 3
PLAYERS = {1: 'X', -1: 'O', 0: ' '}

def _number_to_string(turn):
    return PLAYERS[turn]

def _generate_tictactoe(coordinate):
    "return indices of tictactoe"
    ind_row, ind_col = coordinate
    indices_tictactoe = []
    for delta_1, delta_2 in INDICES_PAIRS:
        indices_tictactoe.append({
            coordinate,
            (ind_row + delta_1[0], ind_col + delta_1[1]),
            (ind_row + delta_2[0], ind_col + delta_2[1]),
        })
    return indices_tictactoe

class ExpandingError(BaseException):
    "Error during node expanding"

class MCTNode(Node):
    """
    MCTS node, inherits from the Node class, extended for MCTS.

    attributes
    ----------
    visits : int,
        Number of visits to this node during MCTS.
    total_score : int,
        Total score accumulated during MCTS simulations.
    """

    def __init__(self, data=None, turn=1, parent=None, depth=0):
        super().__init__(data, turn, parent, depth)
        self.visits = 0
        self.total_score = 0

    def uct_value(self, exploration_weight):
        "Calculate the UCT (Upper Confidence Bound for Trees) value for this node"
        if self.visits == 0:
            return float('inf') if self.turn == 1 else float('-inf')
        exploitation = self.total_score / self.visits
        exploration = exploration_weight * (self.parent.visits / (1 + self.visits))**0.5
        return exploitation + exploration

    def update(self, score):
        "Update visits and total_score based on the result of a simulation"
        self.visits += 1
        self.total_score += score

if __name__ == '__main__':
    # Sample usage of the MCTNode class

    mct_node = MCTNode()
    print(
        f"initial state:\n{mct_node}player: {mct_node.turn}\nis a terminal state: {mct_node.terminated}\nwinner: {mct_node.winner}\n")
