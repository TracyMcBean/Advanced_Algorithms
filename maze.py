import numpy as np
import tree
from random import randrange

class Maze:
    """
    This class can be used to create an instance of maze.

    Private functions:
    __init__, _create_grid, _delete_segment

    Public functions:
    build_maze
    """

    def __init__(self, grid_int, verbose: bool = False):
        """
        Instantiates a new object of class Maze.

        :param grid_int: integer indicating number of rows for grid
        :param verbose: boolean (default: False)
        """
        self._grid_int = grid_int
        self._verbose = verbose
        self._repr = []              # representative of each tree
        self._create_grid()

        # create starting tree for each entry
        for i in range(self._grid_int + 1):
            new_tree = tree.Tree()
            new_tree.add_root(i)
            self._repr.append(new_tree.get_root())

        pass

# ---------------------- private ----------------------------#

    def _create_grid(self):
        """
        Initialize a grid in form of a matrix containing
        Create 2 matrices containing segments (horizontal, vertical).

        """
        # Initialize the inner segments of the grid in matrix with ones.
        grid_minus1 = self._grid_int - 1
        self._seg_horizontal = np.ones((grid_minus1, grid_minus1), dtype=int)
        self._seg_vertical = np.ones((grid_minus1, grid_minus1), dtype=int)

        # Create coordinate for visualization
        self.grid_rows = np.empty([2, self._grid_int, self._grid_int])

        for j in range(self._grid_int):
            row = np.empty([2, self._grid_int])

            for i in range(self._grid_int):
                row[0,i] = i
                row[1,i] = j

            self.grid_rows[:,:,j] = row[:,:]

        pass

    def _delete_segment(self):
        """
        Select and delete a segment if it exists.

        :return: seg_id
        """
        # select what type of segment should be deleted
        # (horizontal = 1, vertical = 2)
        seg_type = randrange(1, 2, 1)
        if seg_type == 1:
            seg_matrix = self._seg_horizontal
        elif seg_type == 2:
            seg_matrix = self._seg_vertical

        # select a segment which should be deleted.
        row_idx = randrange(0, self._grid_int - 1)
        col_idx = randrange(0, self._grid_int - 1)
        entry = seg_matrix[row_idx, col_idx]

        # check if that segment exists (entry=1)
        if entry:
            # if true then delete segment
            seg_id = [row_idx,col_idx]

            if seg_type == 1:
                self._seg_horizontal[row_idx,col_idx] = 0
            else:
                self._seg_vertical[row_idx,col_idx] = 0

            if self._verbose:
                print(entry)
                print("Index of segment to be deleted:" + seg_id)
        else:
            # repeat until a segment is found
            self._delete_segment()

        return seg_id, seg_type;

# ------------------------------ public -------------------------#

    def build_maze(self):
        """
        Create a maze by randomly deleting segments.
        """
        del_seg, seg_type = self._delete_segment()

        # connect the two new neighbors
        if seg_type == 1:
            # horizontal opening
            box1 = del_seg[0]
            box2 = del_seg[0] + 1
        elif seg_type == 2:
            # vertical opening
            box1 = del_seg[1]
            box2 = del_seg[1] + 1

        # find the tree containing the box and return their represenative

        pass

    def get_repr_pos(self):
        return self._repr
