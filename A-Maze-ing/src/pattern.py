"""The "42" pattern: a fixed digit-shaped cluster of fully closed cells.

Per spec (IV.4): the maze must contain a visible "42" drawn by several
fully closed cells, and these cells are explicitly excluded from the
general full-connectivity / no-isolated-cells requirement.

Per spec (PERFECT=False section): the pattern may be omitted if the maze
is too small to fit it. In that case an error message is printed to the
console instead of raising -- this is an expected outcome, not a crash.

This module only computes and stamps the pattern onto a Maze. It does not
run maze generation itself.
"""

from .maze import Maze

# 5 rows x 7 cols dot-matrix bitmap: "4" (3 cols) + 1 col gap + "2" (3 cols).
# '#' marks a cell that must end up fully closed (all 4 walls intact).
# '.' marks a cell the pattern does not touch.
PATTERN_42 = [
    "#.#.###",
    "#.#...#",
    "###.###",
    "..#.#..",
    "..#.###",
]

PATTERN_HEIGHT = len(PATTERN_42)
PATTERN_WIDTH = len(PATTERN_42[0])

# Minimum empty cells to keep between the pattern and the outer border.
MARGIN = 1


def _pattern_cells(anchor_x: int, anchor_y: int) -> set[tuple[int, int]]:
    """Translate the bitmap into absolute (x, y) maze coordinates."""
    cells = set()
    for row_index, row in enumerate(PATTERN_42):
        for col_index, char in enumerate(row):
            if char == "#":
                cells.add((anchor_x + col_index, anchor_y + row_index))
    return cells


def compute_pattern_cells(maze: Maze) -> set[tuple[int, int]] | None:
    """Work out where the "42" pattern should sit, or None if it can't fit.

    Args:
        maze: The (already constructed, not yet generated) Maze.

    Returns:
        The set of (x, y) coordinates the pattern occupies, centred on the
        maze, or None if the maze is too small or the pattern would
        overlap the entry/exit cell. In the None case, the required
        console message has already been printed.
    """
    required_width = PATTERN_WIDTH + 2 * MARGIN
    required_height = PATTERN_HEIGHT + 2 * MARGIN

    if maze.width < required_width or maze.height < required_height:
        print(
            "42 pattern omitted: maze "
            f"{maze.width}x{maze.height} is too small to fit it "
            f"(needs at least {required_width}x{required_height})."
        )
        return None

    anchor_x = (maze.width - PATTERN_WIDTH) // 2
    anchor_y = (maze.height - PATTERN_HEIGHT) // 2

    cells = _pattern_cells(anchor_x, anchor_y)

    if maze.entry in cells or maze.exit in cells:
        print("42 pattern omitted: it would overlap the entry or exit cell.")
        return None

    return cells


def apply_pattern(maze: Maze) -> set[tuple[int, int]] | None:
    """Stamp the "42" pattern onto the maze, if it fits.

    Marks each pattern cell as already-visited so the generation algorithm
    never carves into it -- leaving it fully walled, per spec -- and tags
    it with `is_pattern = True` for later use by rendering/validation
    code.

    Must be called after Maze construction and before generate_maze().

    Args:
        maze: The (already constructed, not yet generated) Maze.

    Returns:
        The set of (x, y) coordinates used, or None if the pattern was
        omitted (see compute_pattern_cells).
    """
    cells = compute_pattern_cells(maze)
    if cells is None:
        return None

    for x, y in cells:
        cell = maze.maze[y][x]
        cell.visited = True
        cell.is_pattern = True

    return cells
