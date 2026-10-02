"""Maze generation and output parser.

Provides recursive backtracking for carving corridors across the grid and
serialization functions to write the maze's hexadecimal wall representation,
entry/exit points, and path instructions to an output text file.
"""
from .maze import Maze
import random


def generate_maze(maze: Maze) -> Maze:
    """Carve corridors through the maze grid using recursive backtracking.

    Iterates through the grid using a randomized depth-first search stack,
    removing separating walls between adjacent unvisited cells.
    Args:
        maze: An empty maze with only closed walls.
    Returns:
        Maze with destroyed walls and carved paths.
    """
    if maze.seed is not None:
        random.seed(maze.seed)

    stack = []

    x = random.randrange(maze.width)
    y = random.randrange(maze.height)

    cur_cell = maze.maze[y][x]
    cur_cell.visited = True

    while True:
        neighbours = maze.get_neighbours(cur_cell)
        unvisited = []
        for cell in neighbours:
            if not cell.visited:
                unvisited.append(cell)

        if unvisited:
            next_cell = random.choice(unvisited)

            maze.remove_wall(cur_cell, next_cell)
            stack.append(cur_cell)
            cur_cell = next_cell
            cur_cell.visited = True
        else:
            if not stack:
                break
            cur_cell = stack.pop()

    return maze


def output(maze: Maze, file_path: str) -> None:
    """Writes output into file (file_path: str)
    Format: Cell stored row by row, one row per line.

    Has a default ./output_maze.txt file_path
    """
    if not file_path:
        file_path = "./output_maze.txt"

    with open(file_path, "w") as file:
        for row in maze.maze:
            for cell in row:
                file.write(format(cell.walls, "x"))
            file.write("\n")
        file.write("\n")
        file.write(str(maze.entry[0]) + "," + str(maze.entry[1]))
        file.write("\n" + str(maze.exit[0]) + "," + str(maze.exit[1]))
        instructions = maze.get_solution_output()
        file.write("\n")
        file.write("".join(instructions))
        file.write("\n")
