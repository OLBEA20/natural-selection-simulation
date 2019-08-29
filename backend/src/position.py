from __future__ import annotations

from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        if type(other) != type(self):
            return False

        if self.x == other.x and self.y == other.y:
            return True

        return False

    def move_right_by(self, step: int) -> Position:
        return Position(bound(self.x + step), self.y)

    def move_left_by(self, step: int) -> Position:
        return Position(bound(self.x - step), self.y)

    def move_up_by(self, step: int) -> Position:
        return Position(self.x, bound(self.y + step))

    def move_down_by(self, step: int) -> Position:
        return Position(self.x, bound(self.y - step))


def bound(value: int):
    return min(39, max(0, value))
