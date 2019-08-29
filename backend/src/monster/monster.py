from __future__ import annotations
from abc import abstractmethod

from src.position import Position
from src.food import Food
from src.world_element import WorldElement
from src.world_elements import WorldElements


class Monster(WorldElement):
    def __init__(self, position: Position):
        self.position = position

    @abstractmethod
    def play_turn(self, monsters: WorldElements[Monster], foods: WorldElements[Food]):
        pass

    def __hash__(self) -> int:
        return super().__hash__()

    def __str__(self) -> str:
        return f"({self.position.x}, {self.position.y})"
