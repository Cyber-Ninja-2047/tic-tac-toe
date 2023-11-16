# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:43:27 2023

@author: f3456221
"""

from tic_tac_toe.node import Node
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
from tic_tac_toe.node_selector import NodeSelector


def initialize_game():
    current_node = Node()
    game_tree = BasicGameTree(current_node)
    node_selector = NodeSelector(game_tree)
    return current_node, node_selector


def choose_a_side():
    while True:
        user_input = input('Enter X or O to choose a side (X|O)"\n')
        if user_input in {"X", "O"}:
            break
    player_side = {"X": 1, "O": -1}[user_input]
    return player_side


def player_move(current_node):
    while True:
        user_input = input('Enter the index to move (row,col):\n')
        inputs = user_input.split(',')
        if len(inputs) != 2:
            continue
        row, col = inputs
        if not (row.isdigit() and col.isdigit()):
            continue
        row = int(row)
        col = int(col)
        if current_node.data[row][col] != 0:
            continue
        break
    index = (row, col)
    current_node = current_node.expand_one(index)
    print(current_node)
    return current_node


def computer_move(node_selector, current_node):
    current_node = node_selector.get_next_node(current_node)
    print(current_node)
    return current_node


def main_function():
    while True:
        current_node, node_selector = initialize_game()
        player_side = choose_a_side()
        if player_side == 1:
            current_node = player_move(current_node)
        while True:
            current_node = computer_move(node_selector, current_node)
            if current_node.terminated == True:
                break
            current_node = player_move(current_node)
            if current_node.terminated == True:
                break

        if current_node.winner == 0:
            print("It's a draw!")
        else:
            if current_node.winner == player_side:
                print("You win!")
            else:
                print("You lose!")

        if input("Play again? (Y|N):\n") != "Y":
            break


if __name__ == '__main__':
    main_function()
