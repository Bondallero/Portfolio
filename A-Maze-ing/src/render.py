"""MiniLibX-based graphical renderer for the maze.

Handles real-time rendering of the maze grid, walls, entry/exit indicators,
shortest path solution, and color themes. Provides key bindings
for toggling the solution, cycling palettes,
regenerating the maze, and exiting.
"""


from .cell import Cell
from .maze import Maze
from mlx.mlx import Mlx  # type: ignore[import-not-found]
from typing import Any
from .backtracker import generate_maze
from .pattern import apply_pattern


class Visualiser:
    """Interactive MiniLibX renderer and event controller for the maze.

    Renders mazes into a fixed-dimension window with adaptive
    cell scaling, drawing walls, solutions,
    and control legends onto an off-screen image buffer.

    Attributes:
        WINDOW_WIDTH: Fixed window pixel width.
        WINDOW_HEIGHT: Fixed window pixel height.
        BOTTOM_BAR_HEIGHT: Reserved height for the bottom legend.
        MIN_CELL_SIZE: Minimum allowable pixel dimensions for a cell.
        MAX_CELL_SIZE: Maximum allowable pixel dimensions for a cell.
        WALL_THICKNESS: Base wall thickness in pixels.
        PALETTES: List of color theme dictionaries.
        maze: The active Maze model instance.
        cell_size: Computed pixel size for each cell.
        wall_thickness: Scaled thickness for rendering walls.
        offset_x: Horizontal centering offset in pixels.
        offset_y: Vertical centering offset in pixels.
        show_path: Boolean flag for solution visibility.
        palette_idx: Index of the currently selected color palette.
    """
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    BOTTOM_BAR_HEIGHT = 67

    MIN_CELL_SIZE = 4
    MAX_CELL_SIZE = 60
    WALL_THICKNESS = 4

    PALETTES = [
        {
            "bg": 0xFFFFFFFF,
            "wall": 0xFF000000,
            "entry": 0xFF00A000,
            "exit": 0xFFD00000,
            "solution": 0xFFFFD54A,
            "pattern": 0xFF202020,
            "text": 0x000000,
        },
        {
            "bg": 0xFF1E1E1E,
            "wall": 0xFFFFFFFF,
            "entry": 0xFF00FF7F,
            "exit": 0xFFFF4500,
            "solution": 0xFF00E5FF,
            "pattern": 0xFF505050,
            "text": 0xFFFFFF,
        },
        {
            "bg": 0xFF2B213A,
            "wall": 0xFFFF71CE,
            "entry": 0xFF01CDFE,
            "exit": 0xFFFF5722,
            "solution": 0xFF05FFA1,
            "pattern": 0xFF433458,
            "text": 0x05FFA1,
        },
        {
            "bg": 0xFF020050,
            "wall": 0xFFEBE600,
            "entry": 0xFF00A000,
            "exit": 0xFFD00000,
            "solution": 0xFFAA2FBB,
            "pattern": 0xFFF50400,
            "text": 0xEBE600,
        },
        {
            "bg": 0xFF75009D,
            "wall": 0xFFFFFFFF,
            "entry": 0xFF00A000,
            "exit": 0xFFD00000,
            "solution": 0xFF00F29D,
            "pattern": 0xFFF50400,
            "text": 0xFFFFFF,
        },
    ]

    def __init__(self, maze: Maze):
        """Initialize the MiniLibX window, image buffer,
        and scaling factors.

        Args:
            maze: The Maze instance to visualize.
        """
        self.maze = maze
        self.width = self.WINDOW_WIDTH
        self.height = self.WINDOW_HEIGHT

        usable_height = self.height - self.BOTTOM_BAR_HEIGHT

        self.cell_size = max(
            self.MIN_CELL_SIZE,
            min(
                self.width // maze.width,
                usable_height // maze.height,
                self.MAX_CELL_SIZE,
            ),
        )
        if (self.width // maze.width < self.MIN_CELL_SIZE
                or usable_height // maze.height < self.MIN_CELL_SIZE):
            print(
                f"Warning: maze {maze.width}x{maze.height} won't fit "
                f"cleanly in available space; "
                f"using minimum cell size ({self.MIN_CELL_SIZE}px)."
            )

        self.wall_thickness = max(
            1, min(self.WALL_THICKNESS, self.cell_size // 15))

        # Centre maze strictly within the upper usable grid area
        maze_px_w = maze.width * self.cell_size
        maze_px_h = maze.height * self.cell_size
        self.offset_x = (self.width - maze_px_w) // 2
        self.offset_y = (usable_height - maze_px_h) // 2

        self.show_path = True
        self.palette_idx = 0

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "A-Maze-ing"
        )
        self.image = self.mlx.mlx_new_image(
            self.mlx_ptr, self.width, self.height
        )
        (
            self.data,
            self.bpp,
            self.line_length,
            self.img_format,
        ) = self.mlx.mlx_get_data_addr(self.image)
        self.bytes_per_pixel = self.bpp // 8

        self._register_hooks()

    @property
    def current_colors(self) -> dict[str, int]:
        """Return the active color scheme dictionary."""
        return self.PALETTES[self.palette_idx]

    def _color_bytes(self, color: int) -> bytes:
        """Convert a 0xAARRGGBB integer to the byte order reported by MiniLibX.

        Args:
            color: Color value in 0xAARRGGBB format.

        Returns:
            A bytes object packed as either BGRA or ARGB
            depending on image format.
        """
        a = (color >> 24) & 0xFF
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        if self.img_format == 0:
            return bytes((b, g, r, a))
        return bytes((a, r, g, b))

    def _fill_rect(
            self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """Fill a solid rectangular area directly in the image buffer.

        Args:
            x0: Left boundary coordinate.
            y0: Top boundary coordinate.
            x1: Right boundary coordinate.
            y1: Bottom boundary coordinate.
            color: Color value in 0xAARRGGBB format.
        """
        color_bytes = self._color_bytes(color)
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.width, x1), min(self.height, y1)
        if x0 >= x1 or y0 >= y1:
            return

        row_bytes = color_bytes * (x1 - x0)
        row_offset = x0 * self.bytes_per_pixel
        row_len = (x1 - x0) * self.bytes_per_pixel

        for y in range(y0, y1):
            base = y * self.line_length + row_offset
            self.data[base:base + row_len] = row_bytes

    def _draw_h_line(self, x0: int, x1: int, y: int,
                     color: int, thickness: int) -> None:
        """Draw a horizontal stroke in the image buffer.

        Args:
            x0: Starting x-coordinate.
            x1: Ending x-coordinate.
            y: Vertical offset.
            color: Color value in 0xAARRGGBB format.
            thickness: Vertical stroke thickness in pixels.
        """
        self._fill_rect(x0, y, x1, y + thickness, color)

    def _draw_v_line(self, x0: int, y0: int, y1: int,
                     color: int, thickness: int) -> None:
        """Draw a vertical stroke in the image buffer.

        Args:
            x0: Horizontal offset.
            y0: Starting y-coordinate.
            y1: Ending y-coordinate.
            color: Color value in 0xAARRGGBB format.
            thickness: Horizontal stroke thickness in pixels.
        """
        self._fill_rect(x0, y0, x0 + thickness, y1, color)

    def _fill_cell(self, x: int, y: int, color: int) -> None:
        """Paint the interior of a specific cell coordinate.

        Args:
            x: Grid column index.
            y: Grid row index.
            color: Fill color in 0xAARRGGBB format.
        """
        cx = self.offset_x + x * self.cell_size
        cy = self.offset_y + y * self.cell_size
        self._fill_rect(cx, cy, cx + self.cell_size,
                        cy + self.cell_size, color)

    def _fill_special_cells(self) -> None:
        """Draw special cell categories including solution,
        pattern, entry, and exit."""
        colors = self.current_colors

        if self.show_path:
            for cell in getattr(self.maze, "solution", []):
                self._fill_cell(cell.x, cell.y, colors["solution"])

        for row in self.maze.maze:
            for cell in row:
                if getattr(cell, "is_pattern", False):
                    self._fill_cell(cell.x, cell.y, colors["pattern"])

        ex, ey = self.maze.entry
        xx, xy = self.maze.exit
        self._fill_cell(ex, ey, colors["entry"])
        self._fill_cell(xx, xy, colors["exit"])

    def _draw_walls(self) -> None:
        """Draw all closed maze walls with overlap
        to eliminate corner gaps."""
        t = self.wall_thickness
        wall_color = self.current_colors["wall"]

        for row in self.maze.maze:
            for cell in row:
                cx = self.offset_x + cell.x * self.cell_size
                cy = self.offset_y + cell.y * self.cell_size

                if cell.has_wall(Cell.north):
                    self._draw_h_line(
                        cx, cx + self.cell_size + t, cy, wall_color, t)
                if cell.has_wall(Cell.west):
                    self._draw_v_line(
                        cx, cy, cy + self.cell_size + t, wall_color, t)

                if (
                    cell.y == self.maze.height - 1
                    and cell.has_wall(Cell.south)
                ):
                    self._draw_h_line(
                        cx, cx + self.cell_size + t,
                        cy + self.cell_size, wall_color, t)
                if (
                    cell.x == self.maze.width - 1
                    and cell.has_wall(Cell.east)
                ):
                    self._draw_v_line(
                        cx + self.cell_size, cy,
                        cy + self.cell_size + t, wall_color, t)

    def _draw_footer(self) -> None:
        """Draw a subtle separator above the legend footer area."""
        bar_top = self.height - self.BOTTOM_BAR_HEIGHT
        self._draw_h_line(
            20, self.width - 20, bar_top, self.current_colors["wall"], 1)

    def _draw_legend(self) -> None:
        """Render keyboard control instructions using
        MiniLibX font blitting."""
        text_color = self.current_colors.get("text", 0xFFFFFF)
        bar_top = self.height - self.BOTTOM_BAR_HEIGHT
        y_pos = bar_top + 30

        legend_items = [
            (80, "[R] Regenerate"),
            (320, "[P] Show/Hide Path"),
            (560, "[C] Change Colors"),
            (800, "[Q / ESC] Exit"),
        ]

        for x_pos, text in legend_items:
            self.mlx.mlx_string_put(
                self.mlx_ptr, self.window,
                x_pos, y_pos,
                text_color, text)

    def render(self) -> None:
        """Render the complete frame into the image buffer
        and put it into the window."""
        self._fill_rect(
            0, 0, self.width, self.height,
            self.current_colors["bg"])
        self._fill_special_cells()
        self._draw_walls()
        self._draw_footer()

        # Copy the image buffer to the window first
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.window, self.image, 0, 0)

        # Draw the text overlay on top
        self._draw_legend()

    def toggle_path(self) -> None:
        """Toggle the shortest path solution display
        and trigger a redraw."""
        self.show_path = not self.show_path
        self.render()

    def cycle_colors(self) -> None:
        """Switch to the next color theme palette and trigger
        a redraw."""
        self.palette_idx = (self.palette_idx + 1) % len(self.PALETTES)
        self.render()

    def regenerate_maze(self) -> None:
        """Reset cells, advance RNG seed, regenerate corridors
        and re-solve."""
        self.maze.maze = [
            [Cell(x, y) for x in range(self.maze.width)]
            for y in range(self.maze.height)
        ]
        self.maze.solution = tuple()

        if self.maze.seed is not None:
            self.maze.seed += 1

        apply_pattern(self.maze)
        generate_maze(self.maze)

        if not getattr(self.maze, "perfect", True):
            self.maze.braid()

        self.maze.solve()
        self.render()

    def _register_hooks(self) -> None:
        """Register MiniLibX event hooks (bindings)
        for window destruction, keys and expose events."""
        self.mlx.mlx_hook(self.window, 33, 0, self._on_close, None)
        self.mlx.mlx_key_hook(self.window, self._on_key, None)
        self.mlx.mlx_expose_hook(self.window, self._on_expose, None)

    def _on_close(self, param: Any) -> None:
        """Handle window close events by terminating the event loop.
        Function is needed to bind window close on Q/ESC buttons."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _on_key(self, keycode: int, param: Any) -> None:
        """Dispatch actions corresponding to pressed keyboard keys.

        Args:
            keycode: Keycode integer received from the window system.
            param: Generic MiniLibX event parameter.
        Result:
            After pressing certain keys visualisation changes
            (adds interactivity to visualisation):
            "P" - Show/Hide solution path;
            "R" - Regenerate the maze;
            "C" - Change color gamma;
            "Q"/"ESC" - close the window.
        """
        if keycode in (65307, 53, 113, 12, ord('x'), ord('X'), 7):
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        elif keycode in (ord('p'), ord('P'), 35):
            self.toggle_path()
        elif keycode in (ord('c'), ord('C'), 8):
            self.cycle_colors()
        elif keycode in (ord('r'), ord('R'), 15):
            self.regenerate_maze()

    def _on_expose(self, param: Any) -> None:
        """Redraw the window when an expose event occurs."""
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.window, self.image, 0, 0)
        self._draw_legend()

    def run(self) -> None:
        """Start the application loop and clean up
        resources upon termination."""
        self.render()
        self.mlx.mlx_loop(self.mlx_ptr)
        self._cleanup()

    def _cleanup(self) -> None:
        """Destroy MiniLibX image, window, and display pointers."""
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.image)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.window)
        self.mlx.mlx_release(self.mlx_ptr)
