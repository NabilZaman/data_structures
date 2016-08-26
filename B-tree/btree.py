#!/usr/bin/env python
"""
btree.py

This file contains an implementation of a B-Tree as outlined in
https://en.wikipedia.org/wiki/B-tree.
"""

class BTree(object):
    """ The BTree class is a 'generic' implementation of a BTree.
        The tree can contain any comparable types.
        The tree is instantiated with a "order" or "branching factor"
        which specifies the maximum number of children any node in the
        tree may have. """

    def __init__(self, order):
        self.order = order

    # More to come?


if __name__ == '__main__':
    test_tree = BTree(3)
    print test_tree
    print test_tree.order
