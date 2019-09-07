import unittest
from unittest.mock import create_autospec

from src.monster.energy import Energy, NotEnoughEnergy
from src.monster.normal_monster import NormalMonster
from src.position import Position
from src.utils.silence import silence
from src.world_elements import PositionAlreadyOccupied, WorldElements

A_POSITION = Position(1, 1)
A_DELTA_POSITION = Position(2, 2)
SOME_ENERGY = Energy(10)
RANGE_OF_MOTION = 1
MONSTER_NAME = "name"
A_MONSTER = NormalMonster(A_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME)


class WorldElementsTest(unittest.TestCase):
    def test_whenRemovingElement_thenElementIsRemoved(self):
        world_elements = WorldElements({A_MONSTER})

        world_elements.remove(A_MONSTER)

        self.assertNotIn(A_MONSTER, world_elements)

    def test_whenMovingElement_thenElementIsRemovedFromPreviousPoisition(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        self.assertNotIn(A_MONSTER, world_elements)

    def test_whenMovingElement_thenElementIsmovedToNewPosition(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        expected_element = NormalMonster(
            A_POSITION + A_DELTA_POSITION, SOME_ENERGY, RANGE_OF_MOTION, MONSTER_NAME
        )
        self.assertIn(expected_element, world_elements)

    def test_whenMovingElement_thenSquaredMagnitudeOfMovementIsRemovedFromEnergy(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        energy.remove.assert_called_once_with(A_DELTA_POSITION.magnitude() ** 2)

    def test_givenNotEnoughEnergy_whenMovingElement_thenExceptionIsRaised(self):
        energy = create_autospec(Energy)
        energy.remove.side_effect = NotEnoughEnergy
        world_elements = WorldElements({A_MONSTER})
        arguments = (A_MONSTER, A_DELTA_POSITION, energy)

        self.assertRaises(NotEnoughEnergy, world_elements.move, *arguments)

    def test_givenNotEnoughEnergy_whenMovingElement_thenElementIsNotMoved(self):
        energy = create_autospec(Energy)
        energy.remove.side_effect = NotEnoughEnergy
        world_elements = WorldElements({A_MONSTER})

        silence(world_elements.move)(A_MONSTER, A_DELTA_POSITION, energy)

        self.assertIn(A_MONSTER, world_elements)

    def test_givenPositionAlreadyOccupied_whenMovingElement_thenExceptionIsRaised(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})
        arguments = (A_MONSTER, Position(0, 0), energy)

        self.assertRaises(PositionAlreadyOccupied, world_elements.move, *arguments)

    def test_givenPositionAlreadyOccupied_whenMovingElement_thenNoMovementHappen(self):
        energy = create_autospec(Energy)
        another_monster = A_MONSTER.move_by(A_DELTA_POSITION)
        world_elements = WorldElements({A_MONSTER, another_monster})

        silence(world_elements.move)(A_MONSTER, A_DELTA_POSITION, energy)

        self.assertIn(A_MONSTER, world_elements)

    def test_givenPositionAlreadyOccupied_whenMovingElement_thenNoEnergyIsWithdrawned(
        self
    ):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        silence(world_elements.move)(A_MONSTER, Position(0, 0), energy)

        energy.remove.assert_not_called()

    def test_givenElementInRange_whenGettingSurroundingElements_thenElementInIterable(
        self
    ):
        range_of_motion = 2
        a_monster_in_range = NormalMonster(
            A_POSITION + Position(range_of_motion - 1, 0),
            SOME_ENERGY,
            range_of_motion,
            MONSTER_NAME,
        )
        world_elements = WorldElements({a_monster_in_range})

        surrouding_elements = world_elements.elements_surrounding(
            A_POSITION, range_of_motion
        )

        self.assertIn(a_monster_in_range, surrouding_elements)

    def test_givenElementNotInRange_whenGettingSurroundingElements_thenElementNotInIterable(
        self
    ):
        range_of_motion = 2
        a_monster_in_range = NormalMonster(
            A_POSITION + Position(range_of_motion + 1, 0),
            SOME_ENERGY,
            range_of_motion,
            MONSTER_NAME,
        )
        world_elements = WorldElements({a_monster_in_range})

        surrouding_elements = world_elements.elements_surrounding(
            A_POSITION, range_of_motion
        )

        self.assertNotIn(a_monster_in_range, surrouding_elements)
