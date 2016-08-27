#!/usr/bin/env python
"""
btree.py

This file contains an implementation of a B-Tree as outlined in
https://en.wikipedia.org/wiki/B-tree.
"""

class BTree(object):
    """ The BTree class is a 'generic' implementation of a BTree.
        The tree can contain any comparable types.
        The tree is instantiated with an "order" or "branching factor"
        which specifies the maximum number of children any node in the
        tree may have. """

    def __init__(self, order, is_root=True):
        self.order = order
        self.keys = []
        self.children = []


    def contains(self, key):
        """ Return whether the tree contains the given key. """
        return False

    def insert(self, key):
        """
        Insert given key into key. Return whether the tree was modified.

        The tree will not be modified if the key was already present.
        """

        return False

    def delete(self, key):
        """
        Remove given key from the tree. Return whether tree was modified.

        The tree will not be modified if the key was not present.
        """

        return False

    def height(self):
        """ Return the height of the tree. """

        return 0

    def is_leaf(self):
        """ Returns whether the tree is a leaf node (has no children)."""
        return not self.children

    def is_empty(self):
        """ Returns whether the tree is empty (has no keys). """
        return not self.keys

    # More to come?


if __name__ == '__main__':
    test_tree = BTree(3)
    print test_tree
    print test_tree.order
