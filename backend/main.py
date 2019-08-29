from time import sleep

from src.food import Food
from src.monster.slow_monster import SlowMonster
from src.position import Position
from src.world import World
from src.world_elements import WorldElements
from src.display.web_world_map import WebWorldMap
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def world_map_constructor(socket: SocketIO):
    def world_map():
        return WebWorldMap(socket)

    return world_map


def run_simulation(socket: SocketIO):
    monster = SlowMonster(Position(0, 30))
    monster_2 = SlowMonster(Position(30, 5))
    monster_3 = SlowMonster(Position(30, 35))
    monster_4 = SlowMonster(Position(10, 0))
    monsters = WorldElements({monster, monster_2, monster_3, monster_4})

    food_1 = Food(Position(1, 1))
    food_2 = Food(Position(3, 3))
    foods = WorldElements({food_1, food_2})

    world = World(monsters, foods, world_map_constructor(socket))
    for _ in range(100):
        world.play_one_day()
        world.display()
        sleep(0.5)


if __name__ == "__main__":
    socketio.start_background_task(run_simulation, socketio)
    socketio.run(app, host="localhost", debug=True)
