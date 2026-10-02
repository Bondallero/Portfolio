from dataclasses import dataclass, field
from collections import deque
from .cell import Cell
import random


@dataclass
class Maze:
    """A grid of cells with entry/exit points.
    Attributes:
        width: Number of cells across.
        height: Number of cells down.
        entry: (x, y) coordinate of the entry cell.
        exit: (x, y) coordinate of the exit cell.
        output_file: Path the generated maze will be written to.
        perfect: Whether the maze must be a perfect maze (single unique
            path between entry and exit, no loops).
        seed: Optional RNG seed for reproducible generation.
        maze: The generated grid of Cell objects, built automatically.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    maze: list[list[Cell]] = field(default_factory=list, init=False)
    solution: tuple[Cell, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers")

        self._validate_coord(self.entry, "ENTRY")
        self._validate_coord(self.exit, "EXIT")
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different cells")

        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y)
                row.append(cell)

            self.maze.append(row)

    def _validate_coord(self, coord: tuple[int, int], label: str) -> None:
        """Raise ValueError if coord falls outside the maze bounds."""
        x, y = coord
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"{label} {coord} is outside the maze bounds "
                f"({self.width}x{self.height})"
            )

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours = []

        y = cell.y
        x = cell.x

        if y > 0:
            neighbours.append(self.maze[y - 1][x])
        if x < self.width - 1:
            neighbours.append(self.maze[y][x + 1])
        if y < self.height - 1:
            neighbours.append(self.maze[y + 1][x])
        if x > 0:
            neighbours.append(self.maze[y][x - 1])

        return neighbours

    def get_avaliable_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours = []

        y = cell.y
        x = cell.x

        if y > 0 and not cell.has_wall(0b0001):
            neighbours.append(self.maze[y - 1][x])
        if x < self.width - 1 and not cell.has_wall(0b0010):
            neighbours.append(self.maze[y][x + 1])
        if y < self.height - 1 and not cell.has_wall(0b0100):
            neighbours.append(self.maze[y + 1][x])
        if x > 0 and not cell.has_wall(0b1000):
            neighbours.append(self.maze[y][x - 1])

        return neighbours

    def remove_wall(self, cell_1: Cell, cell_2: Cell) -> None:
        if cell_1.x < cell_2.x:
            cell_1.remove_wall(Cell.east)
            cell_2.remove_wall(Cell.west)

        elif cell_1.y < cell_2.y:
            cell_1.remove_wall(Cell.south)
            cell_2.remove_wall(Cell.north)

        elif cell_1.y > cell_2.y:
            cell_1.remove_wall(Cell.north)
            cell_2.remove_wall(Cell.south)

        elif cell_1.x > cell_2.x:
            cell_1.remove_wall(Cell.west)
            cell_2.remove_wall(Cell.east)

    def solve(self) -> None:
        start = self.maze[self.entry[1]][self.entry[0]]
        end = self.maze[self.exit[1]][self.exit[0]]
        chain: deque[Cell] = deque([start])
        previous: dict[Cell, Cell | None] = {start: None}

        while chain:
            current = chain.popleft()

            if current == end:
                break

            for neighbour in self.get_avaliable_neighbours(current):
                if neighbour not in previous:
                    previous[neighbour] = current
                    chain.append(neighbour)

        if end not in previous:
            raise ValueError("No way from entry to exit")

        path: list[Cell] = []
        curr: Cell | None = end

        while curr is not None:
            path.append(curr)
            curr = previous[curr]

        path.reverse()
        self.solution = tuple(path)

    def get_solution_output(self) -> list[str]:
        instructions = []

        for i in range(len(self.solution) - 1):
            current = self.solution[i]
            next_cell = self.solution[i + 1]

            if next_cell.y < current.y:
                instructions.append("N")
            elif next_cell.y > current.y:
                instructions.append("S")
            elif next_cell.x < current.x:
                instructions.append("W")
            elif next_cell.x > current.x:
                instructions.append("E")

        return instructions

    def braid(self, braid_p: float = 1.0) -> None:
        """Transforms a perfect maze into an imperfect one
        by removing dead ends.

        braid_p: Probability (0.0 to 1.0) of removing a dead end.
        At 1.0, the maze will have NO dead ends remaining.
        """
        if self.seed is not None:
            random.seed(self.seed)

        dead_ends = []
        for row in self.maze:
            for cell in row:
                if len(self.get_avaliable_neighbours(cell)) == 1:
                    dead_ends.append(cell)

        random.shuffle(dead_ends)

        for cell in dead_ends:
            if len(self.get_avaliable_neighbours(cell)) != 1:
                continue

            # Safe-guard for entry & exit:
            if (cell.x, cell.y) == self.entry or (cell.x, cell.y) == self.exit:
                continue

            if random.random() > braid_p:
                continue

            all_neighbours = self.get_neighbours(cell)
            open_neighbours = self.get_avaliable_neighbours(cell)

            candidates = [candidate for candidate in all_neighbours
                          if candidate not in open_neighbours
                          and not getattr(candidate, "is_pattern", False)]

            if candidates:
                chosen_neighbour = random.choice(candidates)
                self.remove_wall(cell, chosen_neighbour)
