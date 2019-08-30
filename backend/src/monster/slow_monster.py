from __future__ import annotations

import random
from typing import Any, Dict

from src.food import Food
from src.monster.energy import Energy
from src.monster.monster import Monster
from src.position import Position
from src.world_elements import WorldElements, NotEnoughEnergyToMove
from src.world_map import WorldMap


class SlowMonster(Monster):
    def __init__(self, position: Position, energy: Energy):
        super().__init__(position)
        self.energy = energy
        self.possible_moves = [
            Position(1, 0),
            Position(0, 1),
            Position(-1, 0),
            Position(0, -1),
        ]

    def play_turn(self, monsters: WorldElements[Monster], foods: WorldElements[Food]):
        delta_position = random.choice(self.possible_moves)
        try:
            monsters.move(self, delta_position, self.energy)
        except NotEnoughEnergyToMove:
            pass

    def move_by(self, delta_position: Position) -> SlowMonster:
        return SlowMonster(self.position + delta_position, self.energy)

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def _representation(self) -> Dict[str, Any]:
        return {"element_name": self.__class__.__name__, "position": self.position}
