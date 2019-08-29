from typing import Generic, Set, TypeVar

WorldElementSubclass = TypeVar("WorldElement", covariant=True)


class WorldElements(Generic[WorldElementSubclass]):
    def __init__(self, world_elements: Set[WorldElementSubclass]):
        self.world_elements = world_elements
        self.index = 0

    def __iter__(self):
        return iter(list(self.world_elements))

    def __len__(self) -> int:
        return len(self.world_elements)

    def remove(self, element: WorldElementSubclass):
        self.world_elements.remove(element)

    def add(self, element: WorldElementSubclass):
        self.world_elements.add(element)

    def is_empty(self) -> bool:
        return len(self.world_elements) == 0

    def has(self, element: WorldElementSubclass) -> bool:
        result = element in self.world_elements
        return result
