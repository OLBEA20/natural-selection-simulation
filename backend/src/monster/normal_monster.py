from __future__ import annotations

import random
from random import random as generate_fraction
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
        self,
        position: Position,
        energy: Energy,
        range_of_motion: int,
        name: str,
        reproduction_probability: float = 0.25,
    ):
        super().__init__(position)
        self.energy = energy
        self.range_of_motion = range_of_motion
        self.name = name
        self.reproduction_probability = reproduction_probability
        self.possible_moves = [
            Position(range_of_motion, 0),
            Position(0, range_of_motion),
            Position(-range_of_motion, 0),
            Position(0, -range_of_motion),
        ]

    def play_turn(self, monsters: WorldElements[Monster], foods: WorldElements[Food]):
        self._try_to_eat(foods)
        self._try_to_reproduce(monsters)
        self._try_to_move(monsters, foods)

    def _try_to_eat(self, foods: WorldElements[Food]):
        for food in foods.elements_surrounding(self.position, 0):
            food.digest(self.energy)
            foods.remove(food)

    def _try_to_reproduce(self, monsters: WorldElements[Monster]):
        if self._lucky_enough_to_reproduce() and self._has_enough_energy():
            self._reproduce(monsters)

    def _lucky_enough_to_reproduce(self) -> bool:
        return generate_fraction() < self.reproduction_probability

    def _has_enough_energy(self):
        try:
            self.energy.remove(10)
            return True
        except NoMoreEnergy:
            return False

    def _reproduce(self, monsters: WorldElements[Monster]):
        new_monster_position = random.choice(self.possible_moves)
        new_monster = NormalMonster(
            new_monster_position, self.energy.split(), self.range_of_motion, self.name
        )
        monsters.add(new_monster)

    def _try_to_move(
        self, monsters: WorldElements[Monster], foods: WorldElements[Food]
    ):
        movement = self._calculate_movement(foods)
        try:
            monsters.move(self, movement, self.energy)
        except NotEnoughEnergyToMove:
            self._die(monsters)
        except PositionAlreadyOccupied:
            pass

    def _calculate_movement(self, foods: WorldElements[Food]):
        surrounding_foods = foods.elements_surrounding(
            self.position, self.range_of_motion
        )
        for food in surrounding_foods:
            return food.delta_position_from(self.position)
        return random.choice(self.possible_moves)

    def _die(self, monsters: WorldElements[Monster]):
        monsters.remove(self)

    def move_by(self, delta_position: Position) -> NormalMonster:
        new_position = (self.position + delta_position).bound(0, 0)
        return NormalMonster(new_position, self.energy, self.range_of_motion, self.name)

    def display(self, world_map: WorldMap):
        world_map.add_element(self._representation())

    def _representation(self) -> Dict[str, Any]:
        return {"element_name": self.name, "position": self.position}
