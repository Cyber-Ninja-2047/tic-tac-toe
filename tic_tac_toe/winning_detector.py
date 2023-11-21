# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 18:28:22 2023

@author: Anthony

functions to estimate the score for non-terminal states

"""
from tic_tac_toe.node import DIRECTIONS
from itertools import product


class WinningDetector:
    """
    detect the winning patterns for non-terminal nodes

    params
    ------
    size : int,
        the size of the game board
    length : int,
        the length of the winning path

    """

    def __init__(self, size, length):
        self.size = size
        self.length = length
        self._winning_pattern_1 = []
        self._winning_pattern_2 = []
        self.__generate_winning_patterns()

    def detect(self, node):
        """
        detect the number of winner patterns

        params
        ------
        node : Node,
            the node to detect

        returns
        -------
        draw_win_lose : [int, int, int]
            the winning patterns' number of Draw, MAX and MIN

        """
        if node.terminated:
            result = [0, 0, 0]
            result[node.winner] = 1
        else:
            result = list(map(sum, zip(self._check_winning_1(node),
                                       self._check_winning_2(node))))
        return result

    def count_winning_path(self, node):
        "return the number of possible winning path"
        result = [0, 0, 0]
        for player in (-1, 1):
            player_indices = node.coordinates.get(player, set())
            opposite_indices = node.coordinates.get(-player, set())
            for pattern in self._winning_pattern_1:
                if player_indices & pattern and not opposite_indices & pattern:
                    result[player] += 1
        return result

    def __generate_winning_patterns(self):
        "generate the winning patterns of the game in specified size and length"
        for row, col in product(range(self.size), range(self.size)):
            for delta_row, delta_col in DIRECTIONS:
                pattern_1, pattern_2 = self.__generate_winning_index(
                    row, col, delta_row, delta_col)

                if self.__check_pattern_validation(pattern_1):
                    self._winning_pattern_1.append(pattern_1)

                if self.__check_pattern_validation(pattern_2):
                    pattern_2 = self.__convert_pattern_2(pattern_2)
                    self._winning_pattern_2.append(pattern_2)

    def __check_pattern_validation(self, pattern):
        return all(map(self.__check_single_coord, pattern))

    def __check_single_coord(self, coord):
        "check if the coord is valid"
        return 0 <= coord[0] < self.size and 0 <= coord[1] < self.size

    def __generate_winning_index(self, row, col, delta_row, delta_col):
        one_step_patterns = set()  # player will win the game in one step
        two_step_patterns = []  # player will win the game in two steps
        for _ in range(self.length):
            one_step_patterns.add((row, col))
            two_step_patterns.append((row, col))
            row += delta_row
            col += delta_col
        two_step_patterns.append((row, col))
        return one_step_patterns, two_step_patterns

    @staticmethod
    def __convert_pattern_2(pattern_2):
        "convert the format of pattern_2"
        # empty indices, player's indices
        return {pattern_2[0], pattern_2[-1]}, set(pattern_2[1:-1])

    def _check_winning_1(self, node):
        draw_win_lose = [0, 0, 0]
        indices_empty = node.coordinates.get(0, set())

        for player in (-1, 1):
            indices = node.coordinates.get(player, set())
            for pattern_1 in self._winning_pattern_1:
                if (len(pattern_1 & indices_empty) == 1
                        and len(pattern_1 & indices) == self.length - 1):
                    draw_win_lose[player] += 1

        # not the move
        draw_win_lose[-node.turn] = max(0, draw_win_lose[-node.turn] - 1)

        return draw_win_lose

    def _check_winning_2(self, node):
        draw_win_lose = [0, 0, 0]
        indices_empty = node.coordinates.get(0, set())

        for player in (-1, 1):
            indices = node.coordinates.get(player, set())
            for for_empty, for_player in self._winning_pattern_2:
                if (len(for_empty & indices_empty) == 2
                        and len(for_player & indices) == self.length - 1):
                    draw_win_lose[player] += 1

        return draw_win_lose
