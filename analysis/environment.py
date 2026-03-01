from dataclasses import dataclass
from enum import Enum
from random import Random


class Cell(Enum):
    EMPTY = 0
    START = 1
    TARGET = 2
    DEBRIS = 3


@dataclass
class Environment:
    size = None
    debris_ratio = 0.3
    seed = None

    def __init__(self, size, debris_ratio=0.3, seed=None):
        self.size = size
        self.debris_ratio = debris_ratio
        self.seed = seed
        self.__post_init__()

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError("size must be > 0")
        if self.debris_ratio < 0:
            raise ValueError("debris_ratio must be >= 0")

        self._rng = Random(self.seed)
        self.grid = [
            [Cell.EMPTY for _ in range(self.size)] for _ in range(self.size)
        ]
        self.start = (0, 0)
        self.target = (self.size - 1, self.size - 1)

        self._add_start()
        self._add_target()
        self._add_debris()

    def _add_start(self):
        y, x = self.start
        self.grid[y][x] = Cell.START

    def _add_target(self):
        y, x = self.target
        self.grid[y][x] = Cell.TARGET

    def _add_debris(self):
        size = self.size
        target_count = int(self.debris_ratio * size * size)
        placed = 0
        while placed < target_count:
            y = self._rng.randrange(size)
            x = self._rng.randrange(size)
            if self.grid[y][x] == Cell.EMPTY:
                self.grid[y][x] = Cell.DEBRIS
                placed += 1

    def get_adjacent(self, y, x):
        size = self.size
        coords = []
        if y > 0:
            coords.append((y - 1, x))
        if x > 0:
            coords.append((y, x - 1))
        if y + 1 < size:
            coords.append((y + 1, x))
        if x + 1 < size:
            coords.append((y, x + 1))
        return [(ny, nx) for (ny, nx) in coords if self.grid[ny][nx] != Cell.DEBRIS]

    def is_target(self, y, x):
        return self.grid[y][x] == Cell.TARGET

    def make_key(self, y, x):
        return f"{y},{x}"

    def find_target(self):
        return self.target

    def iter_cells(self):
        for y in range(self.size):
            for x in range(self.size):
                yield (y, x), self.grid[y][x]

    def __str__(self):
        def cell_char(cell):
            if cell == Cell.EMPTY:
                return "  "
            if cell == Cell.START:
                return "S "
            if cell == Cell.TARGET:
                return "T "
            return "# "

        lines = []
        for y in range(self.size):
            lines.append("".join(cell_char(self.grid[y][x]) for x in range(self.size)))
        return "\n".join(lines)