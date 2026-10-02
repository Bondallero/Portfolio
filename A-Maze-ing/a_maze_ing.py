"""Entry point for the A-maze-ing generator and visualiser.

Acts as a dispatcher and an assembler for all the created classes, functions,
etc.:
loads maze configurations, stamps the 42 pattern,
carves passages, solves the maze, writes the output representation to disk,
and launches the interactive MiniLibX interface (creates visualisation).
"""
import sys
from src.maze import Maze
from src.config import read_config
from src.backtracker import generate_maze, output
from src.render import Visualiser
from src.pattern import compute_pattern_cells, apply_pattern


def main() -> None:
    """Execute the maze generation and visualisation pipeline.

    Reads the configuration file supplied via command-line arguments,
    initialises and populates the Maze object, exports the state to an
    output file, and starts the visualizer window loop.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    try:
        config = read_config(sys.argv[1])

        maze = Maze(
            width=config["WIDTH"],
            height=config["HEIGHT"],
            entry=config["ENTRY"],
            exit=config["EXIT"],
            output_file=config["OUTPUT_FILE"],
            perfect=config["PERFECT"],
            seed=config["SEED"],
        )
        compute_pattern_cells(maze)
        apply_pattern(maze)
        generate_maze(maze)
        if not maze.perfect:
            maze.braid()
        maze.solve()
        output(maze, maze.output_file)
        visualiser = Visualiser(maze)
        visualiser.run()
    except (ValueError, KeyError, IndexError,
            FileNotFoundError, FileExistsError, PermissionError) as e:
        print(f"Caught error: {e}")


if __name__ == "__main__":
    main()
