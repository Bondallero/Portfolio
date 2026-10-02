from .cell import Cell
from .maze import Maze
from .backtracker import generate_maze


class MazeGenerator:
    """Generates a maze grid and, optionally, a solution path.

    Usage:
        gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14))
        gen.generate()
        gen.solve()
        gen.grid            # list[list[Cell]]
        gen.solution        # list[Cell], entry -> exit
        gen.solution_path() # ["N", "E", "S", ...]
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = True,
        seed: int | None = None,
    ) -> None:
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit
        self._perfect = perfect
        self._seed = seed
        self._maze = self._new_maze()
        self._generated = False

    def _new_maze(self) -> Maze:
        return Maze(
            width=self._width,
            height=self._height,
            entry=self._entry,
            exit=self._exit,
            output_file="",  # unused by mazegen; kept for Maze's shape
            perfect=self._perfect,
            seed=self._seed,
        )

    def generate(self) -> None:
        """Carve the maze. Braids dead ends automatically if perfect=False.

        Safe to call more than once: each call rebuilds a fresh grid from
        scratch rather than re-carving on top of a previous result.
        """
        self._maze = self._new_maze()
        generate_maze(self._maze)
        if not self._maze.perfect:
            self._maze.braid()
        self._generated = True

    def solve(self) -> None:
        """Compute the shortest path from entry to exit (BFS)."""
        if not self._generated:
            raise RuntimeError(
                "Cannot solve before generate(): call generate() first."
            )
        self._maze.solve()

    @property
    def grid(self) -> list[list[Cell]]:
        """The generated grid, indexed grid[y][x]."""
        return self._maze.maze

    @property
    def solution(self) -> tuple[Cell, ...]:
        """The solved path as a list of Cells, entry -> exit."""
        if not self._maze.solution:
            raise RuntimeError(
                "No solution available: call solve() first."
            )
        return self._maze.solution

    def solution_path(self) -> list[str]:
        """The solved path as directional steps: 'N'/'E'/'S'/'W'."""
        return self._maze.get_solution_output()
