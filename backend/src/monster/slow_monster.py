from __future__ import annotations

import random

from src.food import Food
from src.monster.monster import Monster
from src.position import Position
from src.world_elements import WorldElements
from src.world_map import WorldMap


class SlowMonster(Monster):
    def __init__(self, position: Position):
        super().__init__(position)
        self.possible_moves = [
            self.position.move_down_by,
            self.position.move_up_by,
            self.position.move_left_by,
            self.position.move_right_by,
        ]

    def play_turn(self, monsters: WorldElements[Monster], foods: WorldElements[Food]):
        move = random.choice(self.possible_moves)
        monsters.remove(self)
        monsters.add(SlowMonster(move(1)))

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def _representation(self):
        return {"element_name": self.__class__.__name__, "position": self.position}
