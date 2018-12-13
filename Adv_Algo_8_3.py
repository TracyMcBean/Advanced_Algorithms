import maze as mz
import matplotlib.pyplot as plt

"""
Homework for Advanced Algorithms sheet 8 task 3.

Objective:
Build a maze by creating a grid which randomly deletes inner segments.

Known issues:
 + It can happen that the maze ends up being very sparse.
 + Some of the border segments are not plotted correctly.

Date: 13.12.2018
"""

# Set grid size
user_input = False
if user_input:
    n = int(input("Give number >1 of grid boxes for each row"))
    print("Grid size is set to " + str(n) + "x" + str(n))
else:
    n = 60

maze = mz.Maze(n, verbose=False)

plt.figure()
plt.axis('off')

# Basic grid visualized:
for i in range(n+1):
    plt.plot(maze.grid_rows[0, 0:(n+1), i], maze.grid_rows[1, 0:(n+1), i], 'k')
    plt.plot(maze.grid_rows[0, i, 0:(n+1)], maze.grid_rows[1, i, 0:(n+1)], 'k')
plt.title("Maze before deleting segments")

# Build the maze
maze.build_maze()

print("Number of deleted segments:")
print(maze.segment_counter())

print("Visualizing Maze")

# Visualize the maze which was created
points_maze_hor, points_maze_ver = maze.visualize_maze()

plt.figure()
plt.axis('off')

# Border-lines which are not deleted
plt.plot(maze.grid_rows[0, 0:(n+1), n], maze.grid_rows[1, 0:(n+1), n], 'k')
plt.plot(maze.grid_rows[0, 0:(n+1), 0], maze.grid_rows[1, 0:(n+1), 0], 'k')
plt.plot(maze.grid_rows[0, n, 0:(n+1)], maze.grid_rows[1, n, 0:(n+1)], 'k')
plt.plot(maze.grid_rows[0, 0, 0:(n+1)], maze.grid_rows[1, 0, 0:(n+1)], 'k')

# The plotting actually takes most of the time...
i = 0
while i < (len(points_maze_hor)-2):
    # possible speed-up but increases chance that a maze is empty
    # and ((points_maze_hor[i] != [0, 0]).all() or (points_maze_ver[i] != [0, 0]).all()):
    plt.plot(points_maze_hor[i:(i+2), 0], points_maze_hor[i:(i+2), 1], '-k')
    plt.plot(points_maze_ver[i:(i+2), 0], points_maze_ver[i:(i+2), 1], '-k')
    i += 2
plt.title("Maze after deleting segments")

plt.show()
