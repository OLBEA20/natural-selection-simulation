from __future__ import annotations

from abc import ABC, abstractmethod

from src.world_map import WorldMap
from src.position import Position


class WorldElement(ABC):
    def __init__(self, position: Position):
        self.position = position

    @abstractmethod
    def move_by(self, delta_position: Position) -> WorldElement:
        pass

    @abstractmethod
    def display(self, world_map: WorldMap):
        pass

    def distance_from(self, position: Position) -> float:
        return self.delta_position_from(position).magnitude()

    def delta_position_from(self, position: Position) -> Position:
        return self.position - position

    def __hash__(self) -> int:
        return self.position.__hash__()

    def __eq__(self, other: WorldElement) -> bool:
        return self.__hash__() == hash(other)
