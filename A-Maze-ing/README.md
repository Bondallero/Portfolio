*This project has been created as part
of the 42 curriculum by abrzoska, wgulinsk.*
# Description
## Cell structure:
### remove_wall method:
~wall — bitwise NOT (complement)

~ flips every bit: 0s become 1s, 1s become 0s. So if wall = north = 0b1000 (in an 8-bit view for clarity: 0000 1000), then ~wall is 1111 0111 — every bit is 1 except the north bit, which is 0.
(0b is Python's prefix for a binary integer literal — it tells Python "the digits that follow are base-2, not base-10.")

self.walls &= ~wall — bitwise AND, applied in place

& compares bit-by-bit: a bit in the result is 1 only if both operands have a 1 there, otherwise 0. Since ~wall is "all 1s except the wall bit," ANDing self.walls with it means:

every bit that isn't the target wall bit gets ANDed with 1 → unchanged (whatever it was in self.walls, it stays)
the target wall bit gets ANDed with 0 → forced to 0, regardless of what it was before

So the net effect: every wall except the one you're removing is left exactly as it was, and the specified wall bit gets cleared to 0 (open), no matter whether it started open or closed. &= is just Python's shorthand for self.walls = self.walls & ~wall, same as += is shorthand for addition.
## Config validation:
Usage of **TypedDict** from **typing** module allows robust validation and use of mypy friendly *type hints*.
# Instructions
## Configuration file
config.txt contains default maze configuration  
| Key | Description | Example |
| --- | --- | --- |
WIDTH | Maze width (number of cells) | WIDTH=20
HEIGHT | Maze height |HEIGHT=15
ENTRY | Entry coordinates (x,y) | ENTRY=0,0
EXIT | Exit coordinates (x,y) | EXIT=19,14
OUTPUT_FILE | Output filename |OUTPUT_FILE=maze.txt
PERFECT | Is the maze perfect? |PERFECT=True
# Resources
## Maze math
[Wiki - maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)  
[Wiki - maze-solving algorithm](https://en.wikipedia.org/wiki/Maze-solving_algorithm)
## MiniLibX
[42docs -- MiniLibX](https://harm-smits.github.io/42docs/libs/minilibx.html)
# Additions
## mazegen package usage
mazegen contains code that allows you to generate and solve a maze.  
Poetry was used to build mazegen package...
### usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42)
gen.generate()
gen.solve()

# Access the generated structure
for row in gen.grid:
    for cell in row:
        cell.has_wall(cell.north)  # inspect walls

# Access the solution
gen.solution           # list[Cell], entry -> exit
gen.solution_path()    # ['E', 'E', 'S', ...]
```

### Notes
- `perfect=False` automatically braids dead ends during `generate()`.
- Call `generate()` before `solve()` — solving an ungenerated grid raises.

Any required additions will be explicitly listed below.
- The maze generation algorithm you chose.
- Why you chose this algorithm.
- What part of your code is reusable, and how.  
- Your team and project management with:
- Your anticipated planning and how it evolved until the end
- What worked well and what could be improved
- Have you used any specific tools? Which ones? If you implement advanced features (multiple algorithms, display options), describe them in this README.md file.
## Team member roles:
### Władysław
Implementing maze algorithm  
Implementing finding path algorithm  
Implementing MLX tool  
Adding interactive keybinds
Improving Makefile  
Docstring quality control
### Adrian
~~Implementing ASCII rendering~~  
Refactoring code into more pythonic  
Redesigning config parser and validating it  
Implementing MLX library  
Adding scaling functionality to window rendering  
Preparing mazegen package for later use  
Makefile - beta  
Workflow planning and remote managment.  
## Planning and project milestones
0. Planned scope and picked the approach — read the spec, decided on recursive backtracker for perfect-mode generation and BFS for solving/shortest-path, and settled the overall architecture (a src/ layout plus a separate reusable mazegen package). Also weighed and rejected Pydantic for the Maze model in favor of a plain @dataclass with __post_init__, since the project didn't need a validation-record library for a stateful mutable engine.  
1. Stabilized the baseline (config parser, entering the program)
2. Got the mandatory maze logic correct — validated entry/exit, guaranteed full connectivity (including non-perfect mode), kept shared walls coherent after the bit-order fix, and enforced the "no corridor wider than 2 cells" rule.  
3. Implemented both generation modes — perfect mode via recursive backtracker, and non-perfect/Pac-Man mode with open corners + centre, loops, and rare dead-ends — plus the required output format (hex walls, entry/exit coords, BFS shortest path).  
4. Stamped the "42" pattern onto the maze as fully closed cells, filtered out of both dead-end and braid-candidate lists so generation never carves into it.  
5. Built the visual layer — MLX renderer showing walls, entry, exit, and solution path, with regenerate, show/hide-path, and colour-change interactions.  
6. Packaged for reuse — pulled the core logic into a standalone MazeGenerator module (scoped to exclude app-layer concerns like config parsing and rendering), wrote usage docs, and built it into a pip-installable mazegen package with a LICENSE.md.  
7. Hardened and tooled the codebase — Python 3.10+ syntax, full type hints passing mypy, broad exception handling, context managers, flake8-clean, Makefile, .gitignore.  
8. Wrote the README — credits, description, instructions, and resources/AI-disclosure sections in place.  
### comments:
We followed our milestone assumptions and it turned out to be a good workflow. It went mostly smooth beside some small *dead-ends* during development.



