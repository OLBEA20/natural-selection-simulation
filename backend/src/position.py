from __future__ import annotations

from typing import Any, NamedTuple
from math import sqrt


class Position(NamedTuple):
    x: int
    y: int

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):
            return False

        if self.x == other.x and self.y == other.y:
            return True

        return False

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)


def bound(value: int):
    return min(39, max(0, value))
