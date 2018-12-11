import maze as mz
import matplotlib.pyplot as plt
import numpy as np

"""
Homework for Advanced Algorithms sheet 8 task 3.

Objective:
Build a maze by creating a grid which randomly deletes inner segments.


Date: 11.12.2018
"""

n = int(input("Give number of grid boxes for each row"))
print("Grid size is set to " + str(n) + "x" + str(n))

maze = mz.Maze(n)

#plt.figure()
#print(maze.grid_rows)  # dim: array,rows,columns

# Basic grid visualized:

#TODO: Add extra line for outer region!!! Now only inner grid is represented.

for i in range(n):
    plt.plot(maze.grid_rows[0, 0:n, i], maze.grid_rows[1, 0:n, i], 'k')
    plt.plot(maze.grid_rows[0, i, 0:n], maze.grid_rows[1, i, 0:n], 'k')

plt.show()

maze.build_maze()

print(maze.get_repr_pos())
