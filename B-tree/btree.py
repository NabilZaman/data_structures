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

    def __init__(self, order, parent=None, keys=None, children=None):
        if order < 3:
            raise AttributeError("Order must be greater than 2.")
        self.order = order
        self.parent = parent
        if keys is None:
            self.keys = []
        else:
            self.keys = keys
        if children is None:
            self.children = []
        else:
            self.children = children
            for child in self.children:
                child.parent = self

        self.size = len(self.keys) + sum(len(child) for child in self.children)


    def contains(self, key):
        """ Return whether the tree contains the given key. """
        if key in self.keys:
            return True
        elif self.is_leaf:
            return False
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

            self.size += 1
            return True
        else:
            # Recursively insert into appropriate child
            changed = self._find_child_for_key(key).insert(key)
            if changed:
                self.size += 1
            return changed

    def insert_all(self, keys):
        return [self.insert(key) for key in keys]

    def delete(self, key):
        """
        Remove given key from the tree. Return whether tree was modified.

        The tree will not be modified if the key was not present.
        """
        print "Trying to delete", key, "from", self.keys
        if self.is_leaf():
            if key not in self.keys:
                # Nothing to do
                return False
            else:
                # Remove the key and make sure you haven't become too small
                self.keys.remove(key)
                self._merge_if_needed()

                self.size -= 1
                return True
        else:
            if key not in self.keys:
                # Recursively try to delete from appropriate child
                changed = self._find_child_for_key(key).delete(key)
                if changed:
                    self.size -= 1
                return changed
            else:
                replacement_index = find_index_in_sorted_list(key, self.keys)
                # Find a suitable replacement to replace the deleted key
                replacement_child = self.children[replacement_index]
                replacement = replacement_child.find_greatest()
                # Replace the deleted key
                self.keys[replacement_index] = replacement
                # Remove the replacement value from child it came from
                replacement_child.delete(replacement)

                self.size -= 1
                return True

    def delete_all(self, keys):
        return [self.delete(key) for key in keys]

    def height(self):
        """ Return the height of the tree. """
        if self.is_leaf():
            return 1
        return 1 + max(child.height() for child in self.children)

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

    def is_too_empty(self):
        """
        Return whether you have dropped below needed capacity.

        Does not apply to the root node.
        """
        return len(self.keys) < self.order/2 and not self.is_root()

    def find_greatest(self):
        """ Return the greatest key value in the tree. """
        if self.is_leaf():
            return self.keys[-1]
        else:
            return self.children[-1].find_greatest()

    def find_least(self):
        """ Return the least key value in the tree. """
        if self.is_leaf():
            return self.keys[0]
        else:
            return self.children[0].find_least()

    def _merge_if_needed(self):
        """
        Helper function. Merge this node if it is too small.

        Do nothing if the node is not below needed capacity.
        """
        print "Merging if necessary:", self.is_too_empty()
        if self.is_too_empty():
            self.parent._merge_child_with_key(self.keys[0])

    def _merge_child_with_key(self, key):
        """
        Helper function. Increase the size of the child with given key.

        There are two strategies for doing this.
            Firstly you may find a find a sibling with spare keys and
            rotate that siblings extreme key closest to the problem node
            so that that key becomes the new seperator between them and
            the old seperator is inserted into the problem node.
            Secondly if no such sibling can be find, combine this node
            and one of its siblings (that are minimal in size) and add the
            key seperating them to create a new, full-sized node.
        """
        child_index = find_index_in_sorted_list(key, self.keys)
        child = self.children[child_index]
        # First check if there is a child to its right that can donate a key
        if child_index + 1 < len(self.children) and \
            len(self.children[child_index+1].keys) > self.order/2:
            right_child = self.children[child_index+1]
            # Rotate "to the left"
            child.keys.append(self.keys[child_index])
            self.keys[child_index] = right_child.keys[0]
            right_child.delete(right_child.keys[0])
        elif child_index - 1 >= 0 and \
            len(self.children[child_index-1].keys) > self.order/2:
            left_child = self.children[child_index-1]
            # Rotate "to the right"
            self.child.keys.append(self.keys[child_index-1])
            self.keys[child_index-1] = left_child.keys[-1]
            left_child.delete(left_child.keys[-1])
        else:
            if child_index + 1 < len(self.children):
                # Merge with the right_child
                left_child_index = child_index
            else:
                # Merge with the left child
                left_child_index = child_index-1

            right_child_index = left_child_index+1
            left_child = self.children[left_child_index]
            right_child = self.children[right_child_index]
            print "Merging...", left_child.keys, right_child.keys
            # Combine the keys and children of the two children you're merging
            newKeys = left_child.keys + [self.keys.pop(left_child_index)] + \
                right_child.keys
            newChildren = left_child.children + right_child.children

            # Add the new merged child to your list of children
            mergedChild = BTree(self.order, parent=self, keys=newKeys,\
                children=newChildren)
            self.children = self.children[:left_child_index] +\
                [mergedChild] + self.children[right_child_index+1:]

            # Merge yourself if this caused you to grow too small
            self._merge_if_needed()


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
                    keys=self.keys, children=self.children)
                self.keys = []
                self.children = [dummy_child]

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


    def __repr__(self, level=0):
        result = ''
        if self.is_leaf():
            result += '{pre}{keys}\n'.format(pre=level*'\t', keys=self.keys)

        else:
            for index, key in enumerate(self.keys):
                result += '{pre}{child}\n'.format(pre=level*'\t', \
                    child=self.children[index].__repr__(level+1))
                result += '{pre}{key}:\n'.format(pre=level*'\t', key=key)
            result += '{pre}{child}\n'.format(pre=level*'\t', \
                child=self.children[-1].__repr__(level+1))
        return result

    def __len__(self):
        """ Return number of keys in tree. """
        return len(self.keys) + sum(len(child) for child in self.children)

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
    tree.insert_all(range(100))
    tree.delete_all(range(36))
    print len(tree)
    print tree.size
    print tree

    print tree.find_greatest()
    print tree.find_least()
