import numpy as np
from anytree import Node
from random import randrange


class Maze:
    """
    This class can be used to create an instance of maze.
    The maze is built by randomly connecting two boxes.
    The datastructure used, is a general tree containing a
    representative (the root). By using this it is easy to find out
    if two boxes are connected.

    Private functions:
    __init__, _create_grid, _delete_segment

    Public functions:
    build_maze, get_repr_pos, visualize_maze, segment_count
    """

    def __init__(self, grid_int, verbose: bool = False):
        """
        Instantiates a new object of class Maze. The representative
        of each element is stored in an array. The array slot indicates
        the element and the array value is the representative.

        :param grid_int: integer indicating number of rows for grid
        :param verbose: boolean (default: False)
        """
        self._grid_int = grid_int
        self._verbose = verbose      # print extra output if set to True
        self._repr = []              # representative of each tree
        self._segment_count = 0         # how many segments were deleted?

        self._create_grid()          # create the basic grid to start with

        # Initialize root/representative of each box
        for i in range(self._grid_int**2):
            self._repr.append(Node(i))

        pass

# ---------------------- private ----------------------------#

    def _create_grid(self):
        """
        Initialize a grid in form of a matrix containing the segments.
        The entry is set to 1 as long as that segment is not deleted.
        Create 2 matrices containing segments (horizontal, vertical).
        """
        # Initialize the inner segments of the grid in matrix with ones.
        # horizontal number of inner segments : (n-1,n)
        # vertical number of inner segments: (n, n-1)
        grid_minus1 = self._grid_int - 1                                         ### -1
        self._seg_horizontal = np.ones((grid_minus1, self._grid_int), dtype=int)
        self._seg_vertical = np.ones((self._grid_int, grid_minus1), dtype=int)

        # Create coordinate for visualization
        self.grid_rows = np.empty([2, self._grid_int+1, self._grid_int+1])

        for j in range(self._grid_int+1):
            row = np.empty([2, self._grid_int+1])

            for i in range(self._grid_int+1):
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
        entry = 0

        while entry == 0:
            seg_type = randrange(1, 3, 1)
            if seg_type == 1:
                seg_matrix = self._seg_horizontal
                row_idx = randrange(0, self._grid_int-1)
                col_idx = randrange(0, self._grid_int)
            elif seg_type == 2:
                seg_matrix = self._seg_vertical
                row_idx = randrange(0, self._grid_int)
                col_idx = randrange(0, self._grid_int-1)
            entry = seg_matrix[row_idx, col_idx]

        # select an inner segment which should be deleted.
        seg_id = [row_idx,col_idx]

        if self._verbose:
            print("entry:" + str(entry))

        # delete segment by setting its entry to 0
        if seg_type == 1:
            self._seg_horizontal[row_idx,col_idx] = 0
        else:
            self._seg_vertical[row_idx,col_idx] = 0

        # update number of deleted segments
        self._segment_count += 1

        if self._verbose:
            print("Index of segment to be deleted:")
            print(seg_id)
            print("Segment type (horizontal=1 , vertical=2):")
            print(seg_type)

        return seg_id, seg_type

# ------------------------------ public -------------------------#

    def build_maze(self):
        """
        Create a maze by randomly deleting segments. If two boxes are connected
        the first box becomes the parent of the second box and by that its new
        root/representative. If the second box had children then their
        representative is updated to be the first box. And they become children
        of the first box.
        """
        start_end = 1

        """
        The following loop constructs trees with a representative element  
        ( the root ). Every connection of two boxes adds a branch to the   
        tree. As soon as the end and start element are in the tree with the 
        same root, it is clear that they are connected.  
        """
        while start_end:
            # loop only for testing. Set later to while statement
            seg_id, seg_type = self._delete_segment()

            # Find out which boxes will be connected
            box1 = seg_id[0]*self._grid_int + seg_id[1]

            if seg_type == 1:
                # horizontal opening
                box2 = box1 + self._grid_int
                self._seg_horizontal[seg_id[0], seg_id[1]] = 0
            elif seg_type == 2:
                # vertical opening
                box2 = box1 + 1
                
                self._seg_vertical[seg_id[0], seg_id[1]] = 0

            if box1 == box2:
                raise ValueError('Cannot connect same boxes.')
            if (box1 < 0) or (box2 < 0):
                raise ValueError('No negative grid points.')

            if self._verbose:
                print("These are the boxes which are connected: " + str(box1) + " and " + str(box2))
                print("-----Done------")

            # Find the representative of the trees from 2 and 1
            # If equal then do not merge trees.
            if self._repr[box1].root is not self._repr[box2].root:

                if self._verbose:
                    print("boxes root not the same and trees will be merged.")

                # merge trees with box1 root staying root and box2 becoming child.
                self._repr[box2].parent = self._repr[box1]

                # get children of box2 and change their representative
                box2_children = self._repr[box2].descendants

                if box2_children:
                    for i in range(len(box2_children)):
                        child_node = box2_children[i]
                        # Avoid setting a node as its own parent
                        if self._repr[int(child_node.name)] != self._repr[box1]:
                            self._repr[int(child_node.name)].parent = self._repr[box1]
                            self._repr[int(child_node.name)] = self._repr[box1]

                # representative of box2 is now same as box1
                self._repr[box2] = self._repr[box1]

            # check if start and end are connected:
            if self._repr[0].root == self._repr[self._grid_int**2-1].root:
                print("END: Start connected to end")
                start_end = 0

        # end of while loop

        pass

    def get_repr_pos(self):
        """ Get the representatives of each tree."""
        return self._repr

    def visualize_maze(self):
        """
        Create data format to use for the plotting of the maze.
        """
        # filter out horizontal and vertical lines to be drawn
        points_hor = np.zeros((self._grid_int**2, 2), dtype=int)

        r = 0
        for j in range(self._grid_int-1):
            for i in range(self._grid_int):
                if self._seg_horizontal[j, i] == 1:
                    # This looks so silly because np.append didn't do anything

                    points_hor[r, 0] = j
                    points_hor[r, 1] = i+1
                    points_hor[r+1, 0] = j+1
                    points_hor[r+1, 1] = i+1

                    r += 2
                    #np.append(points_hor, [[j+1, i]], axis=0)
                    #np.append(points_hor, [[j+1,i+1]], axis=0)

        # vertical coordinates
        points_ver = np.zeros((self._grid_int ** 2, 2), dtype=int)

        r = 0
        for j in range(self._grid_int):
            for i in range(self._grid_int-1):
                if self._seg_vertical[j, i] == 1:

                    points_ver[r, 0] = j+1
                    points_ver[r, 1] = i
                    points_ver[r + 1, 0] = j+1
                    points_ver[r + 1, 1] = i+1

                    r += 2

        return points_hor, points_ver

    def segment_counter(self):
        """
        Get number of segments that have been deleted.
        :return: self._segment_count
        """
        return self._segment_count
