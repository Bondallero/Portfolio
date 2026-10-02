"""Cell representation and bitmask definitions for maze walls."""


class Cell:
    """A single cell inside the maze grid.

    Maintains coordinate positions, binary wall states represented as a 4-bit
    mask (North, East, South, West).

    Attributes:
        north: Bitmask representing the northern wall (0b0001).
        east: Bitmask representing the eastern wall (0b0010).
        south: Bitmask representing the southern wall (0b0100).
        west: Bitmask representing the western wall (0b1000).
        x: Horizontal grid position (0-indexed from the left).
        y: Vertical grid position (0-indexed from the top).
        walls: Bitfield containing the combination of remaining walls.
        visited: Flag indicating whether DFS or BFS has traversed this cell.
        is_pattern: Flag indicating if the cell is part of the 42 logo.
    """
    north: int = 0b0001
    east: int = 0b0010
    south: int = 0b0100
    west: int = 0b1000

    def __init__(self, x: int, y: int) -> None:
        """Initialize a Cell at the given coordinates with all walls closed.

        Args:
            x: Horizontal coordinate in the maze grid.
            y: Vertical coordinate in the maze grid.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = self.north | self.east | self.south | self.west
        self.visited: bool = False
        self.is_pattern: bool = False

    def remove_wall(self, wall: int) -> None:
        """Remove a specific wall from the cell using bitwise operations.
        Bits are responsible for wall representation (as mentioned
        in previous docstrings).

        Args:
            wall: The directional wall bitmask to clear.
        """
        self.walls &= ~wall

    def has_wall(self, wall: int) -> bool:
        """Check if a specific directional wall is still intact.

        Args:
            wall: The directional wall bitmask to test.

        Returns:
            True if the wall is intact, False if open.
        """
        return self.walls & wall != 0
