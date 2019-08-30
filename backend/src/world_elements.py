from typing import Generic, Set, TypeVar

from src.position import Position
from src.monster.energy import Energy, NoMoreEnergy

WorldElementSubclass = TypeVar("WorldElement", covariant=True)


class WorldElements(Generic[WorldElementSubclass]):
    def __init__(self, world_elements: Set[WorldElementSubclass]):
        self.world_elements = world_elements
        self.index = 0

    def __iter__(self):
        return iter(list(self.world_elements))

    def __len__(self) -> int:
        return len(self.world_elements)

    def _remove(self, element: WorldElementSubclass):
        self.world_elements.remove(element)

    def _add(self, element: WorldElementSubclass):
        self.world_elements.add(element)

    def move(
        self,
        element_to_move: WorldElementSubclass,
        delta_position: Position,
        energy: Energy,
    ):
        try:
            energy.remove(delta_position.magnitude())
            self._move(element_to_move, delta_position)
        except NoMoreEnergy:
            raise NotEnoughEnergyToMove()

    def _move(self, element: WorldElementSubclass, delta_position: Position):
        self._remove(element)
        self._add(element.move_by(delta_position))

    def is_empty(self) -> bool:
        return len(self.world_elements) == 0

    def has(self, element: WorldElementSubclass) -> bool:
        result = element in self.world_elements
        return result


class NotEnoughEnergyToMove(Exception):
    pass
