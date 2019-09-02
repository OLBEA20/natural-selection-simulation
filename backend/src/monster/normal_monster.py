from __future__ import annotations

import random
from random import randint
from typing import Any, Dict

from src.food import Food
from src.monster.energy import Energy, NoMoreEnergy
from src.monster.monster import Monster
from src.position import Position
from src.world_elements import (
    NotEnoughEnergyToMove,
    PositionAlreadyOccupied,
    WorldElements,
)
from src.world_map import WorldMap


class NormalMonster(Monster):
    def __init__(
        self, position: Position, energy: Energy, range_of_motion: int, name: str
    ):
        super().__init__(position)
        self.energy = energy
        self.range_of_motion = range_of_motion
        self.name = name
        self.possible_moves = [
            Position(range_of_motion, 0),
            Position(0, range_of_motion),
            Position(-range_of_motion, 0),
            Position(0, -range_of_motion),
        ]

    def play_turn(self, monsters: WorldElements[Monster], foods: WorldElements[Food]):
        self._try_to_eat(foods)
        self._try_to_reproduce(monsters)
        movement = self._calculate_movement(foods)
        try:
            monsters.move(self, movement, self.energy)
        except NotEnoughEnergyToMove:
            self._die(monsters)
        except PositionAlreadyOccupied:
            pass

    def _try_to_eat(self, foods: WorldElements[Food]):
        food = foods.elements_surrounding(self.position, 0)
        for food in food:
            food.digest(self.energy)
            foods.remove(food)

    def _try_to_reproduce(self, monsters: WorldElements[Monster]):
        if randint(0, 30) > 29:
            try:
                self.energy.remove(10)
            except NoMoreEnergy:
                return
            monsters.add(
                NormalMonster(
                    random.choice(self.possible_moves),
                    self.energy.split(),
                    self.range_of_motion,
                    self.name,
                )
            )

    def _calculate_movement(self, foods: WorldElements[Food]):
        surrounding_foods = foods.elements_surrounding(
            self.position, self.range_of_motion
        )
        for food in surrounding_foods:
            return food.delta_position_from(self.position)
        return random.choice(self.possible_moves)

    def _eat(self, food: Food):
        self.energy.add(food.energy)

    def move_by(self, delta_position: Position) -> NormalMonster:
        new_position = (self.position + delta_position).bound(0, 0)
        return NormalMonster(new_position, self.energy, self.range_of_motion, self.name)

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def _die(self, monsters: WorldElements[Monster]):
        monsters.remove(self)

    def _representation(self) -> Dict[str, Any]:
        return {"element_name": self.name, "position": self.position}
