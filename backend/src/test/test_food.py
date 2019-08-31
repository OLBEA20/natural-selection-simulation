import unittest
from unittest.mock import create_autospec

from src.food import Food
from src.position import Position
from src.monster.energy import Energy

SOME_POSITION = Position(1, 1)


class FoodTest(unittest.TestCase):
    def test_whenDigestingFood_thenEnergyIsTranferred(self):
        energy = create_autospec(Energy)
        food_energy = create_autospec(Energy)
        food = Food(SOME_POSITION, food_energy)

        food.digest(energy)

        energy.add.assert_called_once_with(food_energy)

    def test_whenMovingBy_thenFoodDoesntMove(self):
        energy = create_autospec(Energy)
        some_delta_position = Position(2, 2)
        food = Food(SOME_POSITION, energy)

        moved_food = food.move_by(some_delta_position)

        self.assertEqual(hash(food), hash(moved_food))

    def test_givenFoodsHaveSamePosition_whenCalculatingHashes_thenHashesAreTheSame(
        self
    ):
        energy = create_autospec(Energy)
        food = Food(SOME_POSITION, energy)
        food_2 = Food(SOME_POSITION, energy)

        hash_food = hash(food)
        hash_food_2 = hash(food_2)

        self.assertEqual(hash_food, hash_food_2)

    def test_givenFoodsDontHaveSamePosition_whenCalculatingHashes_thenHashesAreDifferent(
        self
    ):
        energy = create_autospec(Energy)
        food = Food(SOME_POSITION, energy)
        food_2 = Food(SOME_POSITION + SOME_POSITION, energy)

        hash_food = hash(food)
        hash_food_2 = hash(food_2)

        self.assertNotEqual(hash_food, hash_food_2)
