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

    # TODO: write more test statement for expanding


# TODO: write more test case for Node
