import unittest
from unittest.mock import create_autospec

from src.position import Position
from src.monster.slow_monster import SlowMonster
from src.world_elements import WorldElements

STEP = 1


class SlowMonsterTest(unittest.TestCase):
    def test_whenPlayingTurn_thenMonsterMovesByOne(self):
        position = Position(1, 1)
        monster = SlowMonster(position)
        monsters = WorldElements({monster})

        monster.play_turn(monsters, create_autospec(WorldElements))

        self.assertFalse(monsters.has(monster))
        possible_positions = [
            SlowMonster(position.move_down_by(STEP)),
            SlowMonster(position.move_up_by(STEP)),
            SlowMonster(position.move_left_by(STEP)),
            SlowMonster(position.move_right_by(STEP)),
        ]
        self.assertTrue(any(map(monsters.has, possible_positions)))

    def test_whenHashingMonsterWithSamePosition_thenHashesAreTheSame(self):
        monster_1 = SlowMonster(Position(1, 1))
        monster_2 = SlowMonster(Position(1, 1))

        self.assertEqual(hash(monster_1), hash(monster_2))
