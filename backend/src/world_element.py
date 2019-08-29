from __future__ import annotations

from abc import ABC, abstractmethod

from src.world_map import WorldMap
from src.position import Position


class WorldElement(ABC):
    def __init__(self, position: Position):
        self.position = position

    def __hash__(self) -> int:
        return self.position.__hash__()

    def __eq__(self, other: WorldElement) -> bool:
        return self.__hash__() == hash(other)

    @abstractmethod
    def display(self, world_map: WorldMap):
        pass
