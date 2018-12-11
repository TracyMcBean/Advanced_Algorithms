class Tree:
    """
    Class for object of abstract data type general tree.
    Based on a linkend binary tree implementation from
    "Data Structures and Algorithms in Python" by Goodrich et al.
    """

    class _Node:
        """ Nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_children'

        def __init__(self, element, parent=None, children=[]):
            self._element = element
            self._parent = parent
            self._children = children

        def _add_child(self, e):
            """ Add a child e to a node."""
            self._children.append(e)

    class Position:
        """ An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """ Constructor should not be invoked by user"""
            self._container = container
            self._node = node

        def element(self):
            """Return element stored at this position"""
            return self._node._element

# -------------------- construct tree ---------------------- #

    def __init__(self):
        """
        Create an instance tree for a given root.

        """
        self._root = None
        self._size = 0

        pass

# -------------------------- public ------------------------ #

    def __len__(self):
        """Return number of nodes in tree"""
        return self._size

    def is_empty(self, tree):
        """ Check if a tree is empty
        :return empty: bool (True if tree is empty)
        """
        if tree._size == 0:
            empty = False
        else:
            empty = True

        return empty

    def merge_tree(self, tree1, tree2):
        """ Merge two given trees
        :param tree1: 1st tree to be merged
        :param tree2: 2nd tree to be merged
        """

        if not tree1.is_empty():
            new_tree = Tree()
            # TODO: Better check rank and use smaller one as root!
            new_tree._add_root(tree1.get_root)
            new_tree._root._add_child(tree2.get_root)
            # or get_root._add_child etc?

        return new_tree

    def get_root(self):
        return self._make_position(self._root)

    def add_root(self, r):
        """Add a root r"""

        if self._root is not None:
            raise ValueError('Root exists')

        self._size = 1
        self._root = self._Node(r)

        return self._make_position(self._root)
    """
        def find_repr(self,e):
        
        return root
        """

# -------------------- nonpublic ----------------------------------- #

    def _make_position(self, node):
        """ Return position instance for a given node"""
        return self.Position(self, node) if node is not None else None

