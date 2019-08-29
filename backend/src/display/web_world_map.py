from typing import Tuple
import json

from src.world_map import WorldMap
from src.position import Position


class WebWorldMap(WorldMap):
    def __init__(self, socket):
        self.elements = []
        self.socket = socket

    def add_element(self, element: Tuple[str, Position]):
        self.elements.append(element)

    def display(self):
        self.socket.send(json.dumps(self.elements), json=True, namespace="/world_map")
