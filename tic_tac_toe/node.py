# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:11:03 2023

@author: Anthony

A basic component Node on the game tree

"""
from copy import deepcopy


DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]
PLAYERS = {1: 'X', -1: 'O', 0: ' '}


def _number_to_string(turn):
    return PLAYERS[turn]


def generate_tictactoe(coordinate, length):
    "return indices of tictactoe"
    ind_row, ind_col = coordinate
    indices_tictactoe = []
    for delta_row, delta_col in DIRECTIONS:
        index = {(ind_row + delta_row * ind,
                  ind_col + delta_col * ind) for ind in range(length)}
        indices_tictactoe.append(index)
    return indices_tictactoe


class ExpandingError(BaseException):
    "Error during node expanding"


class Node:
    """
    node of the game tree

    params
    ------
    data : nested list or None,
        the current status of board, giving None will return a empty borad
    turn : 1 or -1,
        the current player of this state
    parent : Node or None,
        the parent node of this node, None means a root node
    depth : int,
        the depth of the node, 0 means a root node
    length : int,
        the winning number of marks in a horizontal, vertical, or diagonal row

    attributes
    ----------
    terminated : bool,
        whether this node is a terminal state
    winner : 1, 0 or -1,
        the winner of this state, 0 means no winners
    children : list of Node,
        child nodes of this node
    expanded : bool,
        whether this node is expanded

    """

    def __init__(self, data=None, turn=1, parent=None, depth=0, length=3):
        self._set_data(data)
        self.turn = turn
        self.parent = parent
        self.depth = depth
        self.length = length
        self.children = []
        self.__expanded = False

        self.__get_coordinates()
        self.__check_winner()
        self.__check_terminated()
        self.__get_name()

    def _set_data(self, data):
        if data is None:
            data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.data = data

    @property
    def winner(self):
        "the winner of this state, 0 means no winners"
        return self.__winner

    @property
    def terminated(self):
        "whether this state is a terminal state"
        return self.__terminated

    @property
    def expanded(self):
        "whether this node is expanded"
        return self.__expanded

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, oth):
        return self._name == oth._name and self.turn == oth.turn

    def __lt__(self, oth):
        return self.depth < oth.depth

    def __get_name(self):

        rows = [f'{i} ' + ' '.join(map(_number_to_string, r))
                for i, r in enumerate(self.data)]
        rows.append(
            ' ' * 2 + ' '.join(map(str,
                                   range(len(self.data[-1]))))
        )
        self._name = '\n'.join(rows) + '\n'

    def __get_coordinates(self):
        self.coordinates = {}
        for ind_row, row in enumerate(self.data):
            for ind_col, element in enumerate(row):
                self.coordinates[element] = (
                    self.coordinates.get(element, set()) |
                    {(ind_row, ind_col)})

    def __check_winner(self):
        "check if there is a winner"
        self.__winner = 0
        for player, coordinates in self.coordinates.items():
            if player == 0:
                continue
            if len(coordinates) < self.length:
                continue
            for coordinate in coordinates:
                for ind_tictactoe in generate_tictactoe(coordinate, self.length):
                    if len(ind_tictactoe & coordinates) == self.length:
                        self.__winner = player
                        return

    def __check_terminated(self):
        self.__terminated = True

        # tic-tac-toe!
        if self.winner:
            return

        # board not fulled
        for row in self.data:
            if 0 in row:
                self.__terminated = False
                return

    def clear_children(self):
        "remove all the child nodes"
        self.children.clear()
        self.__expanded = False

    def expand(self):
        "get and return a tuple of child nodes"
        if self.expanded:
            return self.children

        # update the property
        self.__expanded = True

        # dont expand the terminal state
        if self.terminated:
            self.children = []
            return self.children

        # expanding
        children = []
        for index in self.coordinates.get(0, set()):
            node = self.expand_one(index)
            children.append(node)
        self.children = children
        return self.children

    def expand_one(self, index):
        "expand one child node by the given index"
        ind_row, ind_col = index

        # check index
        if self.data[ind_row][ind_col] != 0:
            raise ExpandingError("The space of given index is not empty!")

        # update data
        data = deepcopy(self.data)
        data[ind_row][ind_col] = self.turn
        child = type(self)(data, -self.turn,
                           parent=self,
                           depth=self.depth + 1,
                           length=self.length)
        return child


if __name__ == '__main__':
    # a sample usage of the class Node

    node = Node()
    print(
        f"initial state:\n{node}player: {node.turn}\nis a terminal state: {node.terminated}\nwinner: {node.winner}\n")

    node = node.expand()[0]
    print(
        f"one of the child states:\n{node}player: {node.turn}\nis a terminal state: {node.terminated}\nwinner: {node.winner}\n")

    while not node.terminated:
        node = node.expand()[0]
    print(
        f"one of the terminal states:\n{node}player: {node.turn}\nis a terminal state: {node.terminated}\nwinner: {node.winner}\n")
