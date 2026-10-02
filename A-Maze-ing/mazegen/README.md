## Usage

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