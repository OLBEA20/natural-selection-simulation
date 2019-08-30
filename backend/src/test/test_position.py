import unittest

from math import sqrt
from src.position import Position

X_1 = 1
X_2 = 2
Y_1 = 3
Y_2 = 4


class PositionTest(unittest.TestCase):
    def test_givenSameCoordinates_whenHashingPositions_thenHashesAreTheSame(self):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_1, Y_1)

        self.assertEqual(hash(position_1), hash(position_2))

    def test_givenDifferentCoordinates_whenHashingPositions_thenHashesAreNotTheSame(
        self
    ):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_2, Y_1)

        self.assertNotEqual(hash(position_1), hash(position_2))

    def test_whenAddingPositions_thenCoordinatesAreAddedToEachOther(self):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_2, Y_2)

        actual_position = position_1 + position_2

        expected_position = Position(X_1 + X_2, Y_1 + Y_2)
        self.assertEqual(expected_position, actual_position)

    def test_whenCalculatingMagnitude_thenMagnitudeIsCorrect(self):
        position = Position(X_1, Y_1)

        magnitude = position.magnitude()

        expected_magnitude = sqrt(X_1 * X_1 + Y_1 * Y_1)
        self.assertEqual(expected_magnitude, magnitude)
