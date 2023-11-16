# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:43:27 2023

@author: Paul
"""

from tic_tac_toe.node import Node
from tic_tac_toe.tree.basic_game_tree import BasicGameTree
from tic_tac_toe.node_selector import NodeSelector


NAME_TO_TREE = {
    "minimax": BasicGameTree,
}


def play(**kwargs):
    """
    Play the Tic-Tac-Toe game.

    params
    ------
    size : int,
        The size of the game board. The default is 3.
    tree_type : "minimax", "ab_pruning"
        The type of game tree.

    kwargs
    ------
    Other keyword parameters for game tree.

    """
    # numbers of win, lose and draw for human player
    n_win = n_lose = n_draw = 0
    play_again = True
    root, node_selector = initialize_game(**kwargs)

    while play_again:
        current_node = root
        player_side = choose_a_side()

        # handle the first move
        if player_side == 1:
            current_node = player_move(current_node)

        # game loop
        while True:
            current_node = computer_move(node_selector, current_node)
            if current_node.terminated:
                break
            current_node = player_move(current_node)
            if current_node.terminated:
                break

        if current_node.winner == 0:
            print("It's a draw!")
            n_draw += 1
        else:
            if current_node.winner == player_side:
                print("Congrats! You win!")
                n_win += 1
            else:
                print("Oops, you lose!")
                n_lose += 1

        # print the win-lose ratio
        print(f'Win: {n_win} Draw: {n_draw} Lose: {n_lose}')
        play_again = input("Play again ([Y]/N)? ").upper() != 'N'


def initialize_game(size=3, tree_type="minimax", **kwargs):
    "Initialize the game components"
    root = Node(_generate_empty_board(size))
    clazz = NAME_TO_TREE.get(tree_type, BasicGameTree)
    game_tree = clazz(root, **kwargs)
    node_selector = NodeSelector(game_tree, **kwargs)
    return game_tree.root, node_selector


def _generate_empty_board(size):
    row = [0] * size
    data = [row.copy() for _ in range(size)]
    return data


def choose_a_side():
    "Determine the player side"
    prompt = 'Which side do you want to play (X/O)? '
    while True:
        user_input = input(prompt)
        prompt = 'Invalid input! Please enter "X" or "O" (X/O): '
        user_input = user_input.upper()
        if user_input in {"X", "O"}:
            break
    player_side = {"X": 1, "O": -1}[user_input]
    return player_side


def player_move(current_node):
    prompt = 'Your next move is (row,column)? '
    while True:
        user_input = input(prompt)

        # incase the input is invalid
        prompt = 'Invalid input! Please enter the index as "0,1" (row,column): '
        inputs = user_input.split(',')
        if len(inputs) != 2:
            continue
        row, col = [x.strip() for x in inputs]
        if not (row.isdigit() and col.isdigit()):
            continue
        row = int(row)
        col = int(col)

        # incase the specified space is occupied
        prompt = 'The specified space is occupied! Please enter another index (row,column): '
        try:
            if current_node.data[row][col] != 0:
                continue
        except IndexError:
            prompt = 'Index out of range! Please enter another index (row,column): '
            continue
        break

    index = (row, col)
    current_node = current_node.expand_one(index)
    print(f'--Your Move-----\n{current_node}-----------------')
    return current_node


def computer_move(node_selector, current_node):
    current_node = node_selector.get_next_node(current_node)
    print(f'--Computer Move--\n{current_node}-----------------')
    return current_node


if __name__ == '__main__':
    # sample usage
    play()
