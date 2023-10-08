# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:11:03 2023

@author: mrcho
"""
from copy import deepcopy
from itertools import product


def indices_filter(indices):
    if len(indices) != 2:
        return False
    index_1, index_2 = indices
    return (index_1[0] + index_2[0] == 0 and
            index_1[1] + index_2[1] == 0)


INDICES_DELTA = list(product((-1, 0, 1), (-1, 0, 1)))
INDICES_PAIRS = set(filter(indices_filter, map(
    frozenset, product(INDICES_DELTA, INDICES_DELTA))))
LEN_TICTACTOE = 3
PLAYERS = {1: 'X', -1: 'O', 0: ' '}


def _number_to_string(n):
    return PLAYERS[n]


def check_terminal(node):
    "check if the node is a terminal state"
    # tic-tac-toe!
    if node.winner:
        return True

    # board fulled
    for row in node.data:
        if 0 in row:
            return False
    return True


def _generate_tictactoe(coordinate):
    ind_row, ind_col = coordinate
    indices_tictactoe = []
    for delta_1, delta_2 in INDICES_PAIRS:
        indices_tictactoe.append({
            coordinate,
            (ind_row + delta_1[0], ind_col + delta_1[1]),
            (ind_row + delta_2[0], ind_col + delta_2[1]),
        })
    return indices_tictactoe


class Node:
    "node of the game tree"

    def __init__(self, data, turn, parent=None):
        self.data = data
        self.turn = turn
        self.parent = parent
        self.__get_coordinates()
        self.__check_winner()
        self.__get_name()

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)

    def __get_name(self):
        self._name = '\n'.join([' '.join(map(_number_to_string, r))
                                for r in self.data]) + '\n'

    def __get_coordinates(self):
        self.coordinates = {}
        for ind_row, row in enumerate(self.data):
            for ind_col, element in enumerate(row):
                self.coordinates[element] = (
                    self.coordinates.get(element, set()) |
                    {(ind_row, ind_col)})

    def __check_winner(self):
        "check if there is a winner"
        self.winner = 0
        for player, coordinates in self.coordinates.items():
            if player == 0:
                continue
            if len(coordinates) < LEN_TICTACTOE:
                continue
            for coordinate in coordinates:
                for ind_tictactoe in _generate_tictactoe(coordinate):
                    if len(ind_tictactoe & coordinates) == LEN_TICTACTOE:
                        self.winner = player
                        return

    def expand(self):
        "return children nodes"
        children = []
        for ind_row, ind_col in self.coordinates.get(0, set()):
            data = deepcopy(self.data)
            data[ind_row][ind_col] = self.turn
            node = type(self)(data, -self.turn, parent=self)
            children.append(node)
        return children
