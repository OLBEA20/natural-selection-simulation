import random
from random import randint
from time import sleep, time
from typing import Callable, Tuple

from flask_socketio import SocketIO

from src.display.web_world_map import WebWorldMap
from src.food import Food
from src.monster.energy import Energy
from src.monster.normal_monster import NormalMonster
from src.position import Position
from src.world import World
from src.world_element import WorldElement
from src.world_elements import WorldElements

simulation_running = False


def world_map_constructor(socket: SocketIO):
    def world_map():
        return WebWorldMap(socket)

    return world_map


def generate_world_elements(
    element_constructor: Callable[[Tuple[Position, Energy]], WorldElement],
    number_of_elements: int,
) -> WorldElements:
    position_range = (5, 50)
    world_element_positions = [
        (Position(randint(*position_range), randint(*position_range)), Energy(200))
        for _ in range(number_of_elements)
    ]
    return WorldElements(set(map(element_constructor, world_element_positions)))


class Worker:
    def __init__(self):
        self.running = True

    def run_simulation(self, socket: SocketIO):
        self.running = True
        random.seed(time())
        monsters = generate_world_elements(
            lambda position_energy: NormalMonster(*position_energy, 1, "SlowMonster"),
            randint(5, 15),
        )
        fast_monsters = generate_world_elements(
            lambda position_energy: NormalMonster(*position_energy, 2, "FastMonster"),
            randint(5, 15),
        )
        for monster in fast_monsters:
            monsters.add(monster)

        foods = generate_world_elements(
            lambda position_energy: Food(*position_energy), randint(90, 100)
        )
        world = World(monsters, foods, world_map_constructor(socket))
        for turn in range(500):
            if turn % 10 == 0:
                foods = generate_world_elements(
                    lambda position_energy: Food(*position_energy), randint(20, 30)
                )
                for food in foods:
                    world.foods.add(food)
            world.play_one_day()
            world.display()
            sleep(0.5)

    def stop(self):
        self.running = False
