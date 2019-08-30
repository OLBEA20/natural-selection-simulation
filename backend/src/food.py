from __future__ import annotations

from src.position import Position
from src.world_element import WorldElement
from src.world_map import WorldMap


class Food(WorldElement):
    def __init__(self, position: Position):
        self.position = position

    def __hash__(self) -> int:
        return super().__hash__()

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def move_by(self, delta_position: Position) -> Food:
        return Food(self.position)

    def _representation(self):
        return {"element_name": self.__class__.__name__, "position": self.position}
