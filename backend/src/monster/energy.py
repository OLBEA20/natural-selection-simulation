from __future__ import annotations

from typing import Any


class Energy:
    def __init__(self, value: float):
        self.value: float = value

    def split(self) -> Energy:
        self.value /= 2
        return Energy(self.value)

    def remove(self, value_to_remove: float):
        if self.value <= value_to_remove:
            raise NotEnoughEnergy
        self.value -= value_to_remove

    def add(self, energy: Energy):
        self.value += energy.value
        energy.value = 0

    def __eq__(self, other: Any) -> bool:
        if other and isinstance(other, Energy) and other.value != self.value:
            return False
        return True

    def __ge__(self, other: Energy) -> bool:
        if other is not None and isinstance(other, Energy):
            return self.value >= other.value
        return False


class NotEnoughEnergy(Exception):
    pass
