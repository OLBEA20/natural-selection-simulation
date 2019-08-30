from random import randint
from time import sleep
from typing import Callable

from flask import Flask
from flask_socketio import SocketIO

from src.display.web_world_map import WebWorldMap
from src.food import Food
from src.monster.slow_monster import SlowMonster
from src.position import Position
from src.world import World
from src.world_element import WorldElement
from src.world_elements import WorldElements

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def world_map_constructor(socket: SocketIO):
    def world_map():
        return WebWorldMap(socket)

    return world_map


def generate_world_elements(type: Callable[[Position], WorldElement]) -> WorldElements:
    position_range = (0, 50)
    number_of_elements = randint(2, 2)
    world_element_positions = [
        Position(randint(*position_range), randint(*position_range))
        for _ in range(number_of_elements)
    ]
    return WorldElements(set(map(type, world_element_positions)))


def run_simulation(socket: SocketIO):
    monsters = generate_world_elements(SlowMonster)
    foods = generate_world_elements(Food)
    world = World(monsters, foods, world_map_constructor(socket))

    for _ in range(100):
        world.play_one_day()
        world.display()
        sleep(0.5)


if __name__ == "__main__":
    socketio.start_background_task(run_simulation, socketio)
    socketio.run(app, host="localhost", debug=True)
