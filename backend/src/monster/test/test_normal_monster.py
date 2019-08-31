import unittest

from src.position import Position
from src.monster.energy import Energy
from src.monster.normal_monster import NormalMonster

STEP = 1

X_1 = 1
X_2 = 3
Y_1 = 2
Y_2 = 4

SOME_ENERGY = Energy(10)

RANGE_OF_MOTION = 1
MONSTER_NAME = "name"


class NormalMonsterTest(unittest.TestCase):
    def test_whenHashingMonsterWithSamePosition_thenHashesAreTheSame(self):
        monster_1 = NormalMonster(
            Position(X_1, Y_1), SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )
        monster_2 = NormalMonster(
            Position(X_1, Y_1), SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )

        self.assertEqual(hash(monster_1), hash(monster_2))

    def test_givenDeltaPosition_whenMovingMonster_thenMonsterIsMovedByDeltaPosition(
        self
    ):
        initial_position = Position(X_1, Y_1)
        delta_position = Position(X_2, Y_2)

        moved_monster = NormalMonster(
            initial_position, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        ).move_by(delta_position)

        expected_monster = NormalMonster(
            Position(X_1 + X_2, Y_1 + Y_2), SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )
        self.assertEqual(hash(expected_monster), hash(moved_monster))
