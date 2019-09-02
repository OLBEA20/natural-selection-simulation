from __future__ import annotations

from typing import Any, NamedTuple
from math import sqrt


class Position(NamedTuple):
    x: int
    y: int

    def inverse(self) -> Position:
        return Position(-self.x, -self.y)

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def bound(self, x_bound: int, y_bound: int):
        return Position(max(x_bound, self.x), max(y_bound, self.y))

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):
            return False

        if self.x == other.x and self.y == other.y:
            return True

        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))
