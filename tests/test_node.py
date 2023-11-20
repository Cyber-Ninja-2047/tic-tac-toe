# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 21:50:32 2023

@author: Sharon

Test cases for the component Node

"""
from tic_tac_toe.node import Node


def test_initial_state():
    node = Node()

    # initial board should be empty
    assert node.data == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # first player should be 1
    assert node.turn == 1

    # initial state should not have a winner
    assert not node.winner

    # initial state should not be terminal
    assert not node.terminated


def test_expanding():
    root = Node()
    child_nodes = root.expand()

    # parent of every child node should be the root
    assert all((x.parent == root for x in child_nodes))


def test_node_expand_no_moves():
    data_ls = [[[1, -1, 1], [-1, 1, -1], [1, -1, 1]],
               [[1, -1, 1], [1, -1, -1], [1, -1, 1]],
               [[-1, 1, -1], [1, 1, -1], [1, -1, 1]],
               [[-1, 1, -1], [1, -1, -1], [1, 1, 1]],
               [[1, 1, -1], [-1, 1, -1], [-1, 1, 1]],
               [[1, 1, -1], [1, -1, -1], [1, 1, -1]],
               [[-1, -1, 1], [1, 1, -1], [1, -1, 1]],
               [[-1, -1, -1], [1, -1, -1], [-1, 1, 1]],
               [[1, -1, -1], [1, -1, 1], [1, -1, 1]],
               [[1, -1, -1], [1, 1, -1], [1, -1, 1]]]
    for data in data_ls:
        node = Node(data=data, turn=1)
        children = node.expand()
        assert len(children) == 0


# try to expand a node with available moves
def test_node_expand_with_moves():
    data_ls = [[[-1, 1, -1], [1, 0, -1], [1, 0, 1]],
               [[0, 1, -1], [1, -1, -1], [0, 1, 1]],
               [[1, 0, -1], [0, 1, -1], [-1, 1, 0]],
               [[0, -1, 1], [1, 0, 0], [0, -1, 1]],
               [[0, -1, 0], [0, -1, -1], [-1, 0, 1]],
               [[0, 0, -1], [1, -1, 0], [0, 0, 1]],
               [[0, 0, -1], [1, 0, 0], [0, -1, 1]]]
    for data in data_ls:
        node = Node(data=data, turn=-1)
        children = node.expand()
        assert len(children) > 0


# expand a node and check the return of a child node
def test_node_expand_turn():
    data_ls = [[[1, 0, -1], [-1, 1, -1], [1, -1, 1]],
               [[1, -1, 0], [1, -1, -1], [1, -1, 1]],
               [[-1, 1, -1], [1, 0, -1], [1, 0, 1]],
               [[0, 1, -1], [1, -1, -1], [0, 1, 1]],
               [[1, 0, -1], [0, 1, -1], [-1, 1, 0]],
               [[0, 1, -1], [1, 0, -1], [1, 0, -1]],
               [[0, -1, 1], [1, 0, 0], [0, -1, 1]],
               [[0, -1, 0], [0, -1, -1], [-1, 0, 1]],
               [[0, 0, -1], [1, -1, 0], [0, 0, 1]],
               [[0, 0, -1], [1, 0, 0], [0, -1, 1]]]
    for data in data_ls:
        node = Node(data=data, turn=-1)
        children = node.expand()
        for child in children:
            assert child.turn == 1


# test the termination state with winner == 1
def test_node_termination_winner_a():
    data_ls = [[[1, -1, 1], [-1, 1, -1], [1, -1, 1]],
               [[1, 1, 1], [-1, 1, -1], [1, -1, -1]],
               [[1, -1, -1], [1, 1, -1], [1, -1, 1]],
               [[1, -1, -1], [1, 1, -1], [1, -1, 1]]]
    for data in data_ls:
        node = Node(data=data, turn=-1)
        assert node.terminated == True
        assert node.winner == 1


# test the termination state with winner == -1
def test_node_termination_winner_b():
    data_ls = [[[1, -1, 1], [-1, -1, 1], [1, -1, 0]],
               [[1, 1, -1], [1, -1, 1], [-1, -1, 1]]]
    for data in data_ls:
        node = Node(data=data, turn=-1)
        assert node.terminated == True
        assert node.winner == -1
