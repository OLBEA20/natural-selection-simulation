import unittest
from math import sqrt

from src.position import Position
from src.world_element import WorldElement

X_1 = 1
X_2 = 3
Y_1 = 2
Y_2 = 4


class WorldElementTest(unittest.TestCase):
    def test_whenCalculatingDistanceFromPosition_thenEuclideanDistanceIsReturned(self):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_2, Y_2)
        world_element = WorldElementTestClass(position_1)

        distance = world_element.distance_from(position_2)

        expected_distance = sqrt((X_2 - X_1) ** 2 + (Y_2 - Y_1) ** 2)
        self.assertEqual(expected_distance, distance)

    def test_whenCalculatingDelaPositionFromPosition_thenDeltaPositionIsReturned(self):
        position_1 = Position(X_1, Y_1)
        position_2 = Position(X_2, Y_2)
        world_element = WorldElementTestClass(position_1)

        delta = world_element.delta_position_from(position_2)

        expected_delta = position_1 - position_2
        self.assertEqual(expected_delta, delta)


class WorldElementTestClass(WorldElement):
    def move_by(self, delta_position: Position):
        pass

    def display(self):
        pass
