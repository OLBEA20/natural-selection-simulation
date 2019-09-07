import unittest
from unittest.mock import create_autospec, patch

from src.position import Position
from src.monster.energy import Energy, NotEnoughEnergy
from src.monster.normal_monster import NormalMonster, REPRODUCTION_ENERGY
from src.world_elements import WorldElements, PositionAlreadyOccupied
from src.food import Food

STEP = 1

X_1 = 1
X_2 = 3
Y_1 = 2
Y_2 = 4

SOME_REPRODUCTION_PROBABILITY = 0.1
SOME_ENERGY_VALUE = 10
SOME_FOOD_ENERGY_VALUE = 15
SOME_ENERGY = Energy(SOME_ENERGY_VALUE)

RANGE_OF_MOTION = 1
MONSTER_NAME = "name"
SOME_POSITION = Position(X_1, Y_1)
A_MONSTER = NormalMonster(SOME_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME)
DELTA_POSITION_WITHIN_RANGE = Position(RANGE_OF_MOTION, 0)


class NormalMonsterTest(unittest.TestCase):
    def setUp(self):
        self.monsters_mock = create_autospec(WorldElements)

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

    def test_givenFoodAtMonsterPosition_whenPlayingTurn_thenFoodIsRemoved(self):
        food = Food(SOME_POSITION, SOME_ENERGY)
        foods = WorldElements({food})

        A_MONSTER.play_turn(WorldElements({A_MONSTER}), foods)

        self.assertNotIn(food, foods)

    @patch("src.monster.normal_monster.generate_fraction")
    def test_givenFoodAtMonsterPosition_whenPlayingTurn_thenMonsterGainEnergyFromFood(
        self, generate_fraction
    ):
        generate_fraction.return_value = 2 * SOME_REPRODUCTION_PROBABILITY
        food_energy = Energy(SOME_FOOD_ENERGY_VALUE)
        food = Food(SOME_POSITION, food_energy)
        monster_energy = Energy(SOME_ENERGY_VALUE)
        monster = NormalMonster(
            SOME_POSITION,
            monster_energy,
            RANGE_OF_MOTION,
            MONSTER_NAME,
            SOME_REPRODUCTION_PROBABILITY,
        )

        monster.play_turn(self.monsters_mock, WorldElements({food}))

        expected_energy = Energy(SOME_FOOD_ENERGY_VALUE)
        expected_energy.add(Energy(SOME_ENERGY_VALUE))
        self.assertEqual(expected_energy, monster_energy)

    @patch("src.monster.normal_monster.generate_fraction")
    def test_givenNoFoodsAtMonsterPosition_whenPlayingTurn_thenMonsterDoesnGainEnergy(
        self, generate_fraction
    ):
        generate_fraction.return_value = 2 * SOME_REPRODUCTION_PROBABILITY
        food = Food(SOME_POSITION + SOME_POSITION, SOME_ENERGY)
        monster_energy = Energy(SOME_ENERGY_VALUE)
        monster = NormalMonster(
            SOME_POSITION,
            monster_energy,
            RANGE_OF_MOTION,
            MONSTER_NAME,
            SOME_REPRODUCTION_PROBABILITY,
        )

        monster.play_turn(self.monsters_mock, WorldElements({food}))

        expected_energy = Energy(SOME_ENERGY_VALUE)
        self.assertEqual(expected_energy, monster_energy)

    def test_givenFoodSurroundingMonster_whenPlayingTurn_thenMonsterMoveTowardFood(
        self
    ):
        food = Food(SOME_POSITION + DELTA_POSITION_WITHIN_RANGE, SOME_ENERGY)
        monster = NormalMonster(
            SOME_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )

        monster.play_turn(self.monsters_mock, WorldElements({food}))

        expected_movement = food.delta_position_from(monster.position)
        self.monsters_mock.move.assert_called_once_with(
            monster, expected_movement, SOME_ENERGY
        )

    def test_givenNoFoodsSurroundingMonster_whenPlayingTurn_thenMonsterMovesAnyWhere(
        self
    ):
        monster = NormalMonster(
            SOME_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.move.assert_called_once_with(
            monster, Not(Position(0, 0)), SOME_ENERGY
        )

    def test_givenMonsterDoesntHaveEnoughEnergyToMove_whenPlayingTurn_thenMonsterDies(
        self
    ):
        monster = NormalMonster(
            SOME_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )
        self.monsters_mock.move.side_effect = NotEnoughEnergy

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.remove.assert_called_once_with(monster)

    def test_givenMonsterWantsToMoveIntoAnOccupiedPosition_whenPlayingTurn_thenMonsterDoesntMove(
        self
    ):
        monster = NormalMonster(
            SOME_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )
        self.monsters_mock.move.side_effect = PositionAlreadyOccupied

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.move.assert_called_once()

    @patch("src.monster.normal_monster.generate_fraction")
    def test_givenMonsterHasChanceToReproduceAndEnoughEnergy_whenPlayingTurn_thenMonsterReproduces(
        self, generate_fraction
    ):
        generate_fraction.return_value = SOME_REPRODUCTION_PROBABILITY / 2
        enough_energy_to_reproduce = Energy(REPRODUCTION_ENERGY + 1)
        monster = NormalMonster(
            SOME_POSITION,
            enough_energy_to_reproduce,
            RANGE_OF_MOTION,
            MONSTER_NAME,
            SOME_REPRODUCTION_PROBABILITY,
        )

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.add.assert_called_once()

    @patch("src.monster.normal_monster.generate_fraction")
    def test_givenMonsterHasChanceToReproduceButNotEnoughEnergy_whenPlayingTurn_thenMonsterDoesntReproduces(
        self, generate_fraction
    ):
        generate_fraction.return_value = SOME_REPRODUCTION_PROBABILITY / 2
        enough_energy_to_reproduce = Energy(REPRODUCTION_ENERGY - 1)
        monster = NormalMonster(
            SOME_POSITION,
            enough_energy_to_reproduce,
            RANGE_OF_MOTION,
            MONSTER_NAME,
            SOME_REPRODUCTION_PROBABILITY,
        )

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.add.assert_not_called()

    @patch("src.monster.normal_monster.generate_fraction")
    def test_givenMonsterDoesntHaveChanceToReproduce_whenPlayingTurn_thenMonsterDoesntReproduces(
        self, generate_fraction
    ):
        generate_fraction.return_value = 2 * SOME_REPRODUCTION_PROBABILITY
        enough_energy_to_reproduce = Energy(10 - 1)
        monster = NormalMonster(
            SOME_POSITION,
            enough_energy_to_reproduce,
            RANGE_OF_MOTION,
            MONSTER_NAME,
            SOME_REPRODUCTION_PROBABILITY,
        )

        monster.play_turn(self.monsters_mock, WorldElements(set()))

        self.monsters_mock.add.assert_not_called()


def Not(element):
    class Not:
        def __init__(self):
            pass

        def __eq__(self, other):
            return element != other

    return Not()
