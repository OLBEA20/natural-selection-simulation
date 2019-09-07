from typing import Tuple
import json

from src.world_map import WorldMap


class WebWorldMap(WorldMap):
    def __init__(self, socket):
        self.elements = []
        self.socket = socket

    def add_element(self, element: Tuple[str, Tuple[int, int]]):
        self.elements.append(element)

    def display(self):
        self.socket.send(json.dumps(self.elements), json=True, namespace="/simulation")
