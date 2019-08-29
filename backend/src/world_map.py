from abc import ABC, abstractmethod
from typing import Dict

from src.position import Position


class WorldMap(ABC):
    @abstractmethod
    def add_element(self, element: Dict[str, Position]):
        pass

    @abstractmethod
    def display(self):
        pass
