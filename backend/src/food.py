from __future__ import annotations
from typing import Any, Dict

from src.position import Position
from src.monster.energy import Energy
from src.world_element import WorldElement
from src.world_map import WorldMap


class Food(WorldElement):
    def __init__(self, position: Position, energy: Energy):
        self.position = position
        self.energy = energy

    def __hash__(self) -> int:
        return super().__hash__()

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def move_by(self, delta_position: Position) -> Food:
        return Food(self.position, self.energy)

    def digest(self, energy: Energy):
        energy.add(self.energy)

    def _representation(self) -> Dict[str, Any]:
        return {"element_name": self.__class__.__name__, "position": self.position}
