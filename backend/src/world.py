from typing import Callable

from src.food import Food
from src.monster.monster import Monster
from src.world_elements import WorldElements
from src.world_map import WorldMap


class World:
    def __init__(
        self,
        monsters: WorldElements[Monster],
        foods: WorldElements[Food],
        world_map_constructor: Callable[[], WorldMap],
    ):
        self.monsters = monsters
        self.foods = foods
        self.world_map_constructor = world_map_constructor

    def play_one_day(self):
        for monster in self.monsters:
            monster.play_turn(self.monsters, self.foods)

    def display(self):
        world_map = self.world_map_constructor()
        for monster in self.monsters:
            monster.display(world_map)
        for food in self.foods:
            food.display(world_map)
        world_map.display()
