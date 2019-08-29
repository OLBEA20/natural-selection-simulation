import unittest

from src.position import Position

X_1 = 1
Y_1 = 3

STEP = 1


class PositionTest(unittest.TestCase):
    def test_givenSameCoordinate_whenHashingPositions_thenHashesAreTheSame(self):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_1, Y_1)

        self.assertEqual(hash(position_1), hash(position_2))

    def test_givenDifferentAbscissa_whenHashingPositions_thenHashesAreNotTheSame(self):
        position_1 = Position(X_1, Y_1)
        position_2 = position_1.move_right_by(1)

        self.assertNotEqual(hash(position_1), hash(position_2))

    def test_givenDifferentOrdinate_whenHashingPositions_thenHashesAreNotTheSame(self):
        position_1 = Position(X_1, Y_1)
        position_2 = position_1.move_up_by(1)

        self.assertNotEqual(hash(position_1), hash(position_2))

    def test_whenMovingToTheRight_thenAbscissaIsIncreased(self):
        position_1 = Position(X_1, Y_1)

        position_to_the_rigth = position_1.move_right_by(STEP)

        self.assertEqual(X_1 + STEP, position_to_the_rigth.x)

    def test_whenMovingToTheLeft_thenAbscissaIsDecreased(self):
        position_1 = Position(X_1, Y_1)

        position_to_the_rigth = position_1.move_left_by(STEP)

        self.assertEqual(X_1 - STEP, position_to_the_rigth.x)

    def test_whenMovingUp_thenOrdinateIsIncreased(self):
        position_1 = Position(X_1, Y_1)

        position_to_the_rigth = position_1.move_up_by(STEP)

        self.assertEqual(Y_1 + STEP, position_to_the_rigth.y)

    def test_whenMovingDown_thenOrdinateIsIncreased(self):
        position_1 = Position(X_1, Y_1)

        position_to_the_rigth = position_1.move_down_by(STEP)

        self.assertEqual(Y_1 - STEP, position_to_the_rigth.y)
