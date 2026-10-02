class Cell:
    north: int = 0b0001
    east: int = 0b0010
    south: int = 0b0100
    west: int = 0b1000

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = self.north | self.east | self.south | self.west
        self.visited: bool = False
        self.is_pattern: bool = False

    def remove_wall(self, wall: int) -> None:
        self.walls &= ~wall

    def has_wall(self, wall: int) -> bool:
        return self.walls & wall != 0
