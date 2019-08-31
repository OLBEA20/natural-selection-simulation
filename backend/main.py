from random import randint
from time import sleep
from typing import Callable, Tuple

from flask import Flask
from flask_socketio import SocketIO

from src.display.web_world_map import WebWorldMap
from src.food import Food
from src.monster.normal_monster import NormalMonster
from src.monster.energy import Energy
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


def generate_world_elements(
    element_constructor: Callable[[Tuple[Position, Energy]], WorldElement],
    number_of_elements: int,
) -> WorldElements:
    position_range = (0, 50)
    world_element_positions = [
        (Position(randint(*position_range), randint(*position_range)), Energy(200))
        for _ in range(number_of_elements)
    ]
    return WorldElements(set(map(element_constructor, world_element_positions)))


def run_simulation(socket: SocketIO):
    monsters = generate_world_elements(
        lambda position_energy: NormalMonster(*position_energy, 1, "SlowMonster"),
        randint(5, 15),
    )
    print(f"Spawning {len(monsters)} SlowMonster")
    fast_monsters = generate_world_elements(
        lambda position_energy: NormalMonster(*position_energy, 2, "FastMonster"),
        randint(5, 15),
    )
    print(f"Spawning {len(fast_monsters)} FastMonster")
    for monster in fast_monsters:
        monsters.add(monster)
    foods = generate_world_elements(
        lambda position_energy: Food(*position_energy), randint(20, 25)
    )
    print(f"Spawning {len(foods)} Food")
    world = World(monsters, foods, world_map_constructor(socket))

    for _ in range(500):
        world.play_one_day()
        world.display()
        sleep(0.5)


if __name__ == "__main__":
    socketio.start_background_task(run_simulation, socketio)
    socketio.run(app, host="localhost", debug=True)
