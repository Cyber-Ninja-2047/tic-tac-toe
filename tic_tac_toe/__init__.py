# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:37:43 2023

@author: Anthony
"""
import sys
import argparse
from tic_tac_toe.play import play


def main():
    "Execute"
    args = init_args()
    play(size=args.size, length=args.length, tree_type=args.tree)


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', required=False,
                        help='Size of the game board. The default is 3.',
                        default=3, type=int)
    parser.add_argument('-l', '--length', required=False,
                        help='The winning number of marks in a horizontal, vertical, or diagonal row',
                        default=3, type=int)
    parser.add_argument('-t', '--tree', required=False,
                        help='The type of game tree. The default is "minimax"',
                        default="minimax", type=str)
    return parser.parse_args(sys.argv[1:])
