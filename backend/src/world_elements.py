from typing import Generic, Iterable, Set, TypeVar

from src.position import Position
from src.monster.energy import Energy, NoMoreEnergy

WorldElementSubclass = TypeVar("WorldElement", covariant=True)


class WorldElements(Generic[WorldElementSubclass]):
    def __init__(self, world_elements: Set[WorldElementSubclass]):
        self.world_elements = world_elements
        self.index = 0

    def elements_surrounding(
        self, position: Position, surrounding_range: float
    ) -> Iterable[WorldElementSubclass]:
        def element_distance_inside_range(element: WorldElementSubclass):
            return element.distance_from(position) <= surrounding_range

        return list(filter(element_distance_inside_range, self.world_elements))

    def remove(self, element: WorldElementSubclass):
        self.world_elements.remove(element)

    def add(self, element: WorldElementSubclass):
        self.world_elements.add(element)

    def move(
        self,
        element_to_move: WorldElementSubclass,
        delta_position: Position,
        energy: Energy,
    ):
        try:
            self._move(element_to_move, delta_position)
            energy.remove(delta_position.magnitude() ** 2)
        except NoMoreEnergy:
            self._move(
                element_to_move.move_by(delta_position), delta_position.inverse()
            )
            raise NotEnoughEnergyToMove()

    def _move(self, element: WorldElementSubclass, delta_position: Position):
        if element.move_by(delta_position) in self.world_elements:
            raise PositionAlreadyOccupied
        self.remove(element)
        self.add(element.move_by(delta_position))

    def has(self, element: WorldElementSubclass) -> bool:
        result = element in self.world_elements
        return result

    def __iter__(self):
        return iter(list(self.world_elements))

    def __len__(self) -> int:
        return len(self.world_elements)


class NotEnoughEnergyToMove(Exception):
    pass


class PositionAlreadyOccupied(Exception):
    pass
