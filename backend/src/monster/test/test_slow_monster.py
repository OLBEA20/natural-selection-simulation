import unittest

from src.position import Position
from src.monster.energy import Energy
from src.monster.slow_monster import SlowMonster

STEP = 1

X_1 = 1
X_2 = 3
Y_1 = 2
Y_2 = 4

SOME_ENERGY = Energy(10)


class SlowMonsterTest(unittest.TestCase):
    def test_whenHashingMonsterWithSamePosition_thenHashesAreTheSame(self):
        monster_1 = SlowMonster(Position(X_1, Y_1), SOME_ENERGY)
        monster_2 = SlowMonster(Position(X_1, Y_1), SOME_ENERGY)

        self.assertEqual(hash(monster_1), hash(monster_2))

    def test_givenDeltaPosition_whenMovingMonster_thenMonsterIsMovedByDeltaPosition(
        self
    ):
        initial_position = Position(X_1, Y_1)
        delta_position = Position(X_2, Y_2)

        moved_monster = SlowMonster(initial_position, SOME_ENERGY).move_by(
            delta_position
        )

        expected_monster = SlowMonster(Position(X_1 + X_2, Y_1 + Y_2), SOME_ENERGY)
        self.assertEqual(hash(expected_monster), hash(moved_monster))
