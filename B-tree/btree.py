#!/usr/bin/env python
"""
btree.py

This file contains an implementation of a B-Tree as outlined in
https://en.wikipedia.org/wiki/B-tree.
"""

def find_index_in_sorted_list(key, L):
    """
    Helper function. Return index closest (above) key in sorted list.
    """
    if not L:
        return 0
    if len(L) == 1:
        if key > L[0]:
            return 1
        else:
            return 0

    halfway = len(L) / 2
    if key < L[halfway]:
        return find_index_in_sorted_list(key, L[:halfway])
    else:
        return halfway + find_index_in_sorted_list(key, L[halfway:])


class BTree(object):
    """ The BTree class is a 'generic' implementation of a BTree.
        The tree can contain any comparable types.
        The tree is instantiated with an "order" or "branching factor"
        which specifies the maximum number of children any node in the
        tree may have. """

    def __init__(self, order, parent=None, keys=[], children=[]):
        if order < 1:
            raise AttributeError("Order must be a positive integer.")
        self.order = order
        self.parent = parent
        self.keys = keys
        self.children = children


    def contains(self, key):
        """ Return whether the tree contains the given key. """
        if key in self.keys:
            return True
        else:
            return self._find_child_for_key(key).contains(key)

    def insert(self, key):
        """
        Insert given key into key. Return whether the tree was modified.

        The tree will not be modified if the key was already present.
        """
        if key in self.keys:
            return False

        if self.is_leaf():
            # Simply add the key to your keys
            self.keys.append(key)
            self.keys.sort()

            # Then make sure you haven't become too large
            self._split_if_needed()

            return True
        else:
            # Recursively insert into appropriate child
            return self._find_child_for_key(key).insert(key)

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
        """ Return whether the tree is a leaf node (has no children). """
        return not self.children

    def is_root(self):
        """ Return whether this tree is the root node (has no parent). """
        return self.parent is None

    def is_empty(self):
        """ Return whether the tree is empty (has no keys). """
        return not self.keys

    def is_too_full(self):
        """ Return whether you have exceeded capacity. """
        return len(self.keys) >= self.order

    def _split_if_needed(self):
        """
        Helper function. Split this node if it is too large.

        Do nothing if the node does not exceed capacity.
        Mutually recurse with _split_child_with_key.
        """

        if self.is_too_full():
            # Need to split the node
            half_keys = len(self.keys) / 2
            median = self.keys[half_keys]
            self.keys = self.keys[:half_keys] + self.keys[half_keys+1:]
            if self.is_root():
                # Need to split yourself
                dummy_child = BTree(self.order, parent=self,\
                    keys=self.keys, children=[])
                self.keys = []
                self.children.append(dummy_child)

                self._split_child_with_key(median)

            else:
                # Get your parent to split you
                self.parent._split_child_with_key(median)


    def _split_child_with_key(self, key):
        """
        Helper function. Split a "full" child node into two children.

        Find the child the key would belong to, splits that child in half,
        then uses that key as the seperator between those two new children.

        Mutually recurse with _split_if_needed.
        """
        # Find the child
        child_index = find_index_in_sorted_list(key, self.keys)
        child = self.children[child_index]

        # Split its keys and children
        half_keys = len(child.keys) / 2
        left_half_keys = child.keys[:half_keys]
        right_half_keys = child.keys[half_keys:]

        half_children = len(child.children) / 2
        left_half_children = child.children[:half_children]
        right_half_children = child.children[half_children:]

        # Build two new children each with half its resources
        newLeftChild = BTree(self.order, parent=self, \
            keys=left_half_keys, children=left_half_children)
        newRightChild = BTree(self.order, parent=self, \
            keys=right_half_keys, children=right_half_children)

        # Fill in your keys/children with these new ones
        self.keys = self.keys[:child_index] + [key] + self.keys[child_index:]
        self.children = self.children[:child_index] + \
            [newLeftChild, newRightChild] + \
            self.children[child_index+1:]

        # Split yourself if this caused you to grow too large
        self._split_if_needed()

    def _find_child_for_key(self, key):
        """
        Helper function. Return the child that is responsible for the given key.

        Key can not be in this node.
        """
        child_index = find_index_in_sorted_list(key, self.keys)
        return self.children[child_index]


    def __str__(self, prefix=''):
        result = ''
        if self.is_leaf():
            for index, key in enumerate(self.keys):
                result += '{pre}{key}:\n'.format(pre=prefix, key=key)

        else:
            for index, key in enumerate(self.keys):
                result += '{pre} {child}\n'.format(pre=prefix, \
                    child=self.children[index].__str__(prefix + '\t'))
                result += '{pre} {key}:\n'.format(pre=prefix, key=key)
            result += '{pre} {child}\n'.format(pre=prefix, \
                child=self.children[-1].__str__(prefix + '\t'))
        return result
        # More to come?

if __name__ == '__main__':
    test_list1 = [1, 3, 5, 7, 9, 11, 13]
    test_list2 = [2, 4, 6, 8, 10, 12]
    test_list3 = [1]

    keys = [0, 2, 6, 9, 15]
    print [(find_index_in_sorted_list(key, test_list1), key) for key in keys]
    print [(find_index_in_sorted_list(key, test_list2), key) for key in keys]
    print [(find_index_in_sorted_list(key, test_list3), key) for key in keys]

    tree = BTree(5)
    [tree.insert(val) for val in range(40, 140, 2)]
    print tree
