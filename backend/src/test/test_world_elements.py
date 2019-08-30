import unittest
from unittest.mock import create_autospec

from src.position import Position
from src.monster.slow_monster import SlowMonster
from src.monster.energy import Energy, NoMoreEnergy
from src.world_elements import WorldElements, NotEnoughEnergyToMove

A_POSITION = Position(1, 1)
A_DELTA_POSITION = Position(2, 2)
SOME_ENERGY = Energy(10)
A_MONSTER = SlowMonster(A_POSITION, SOME_ENERGY)


class WorldElementsTest(unittest.TestCase):
    def test_whenMovingElement_thenElementIsRemovedFromPreviousPoisition(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        self.assertNotIn(A_MONSTER, world_elements)

    def test_whenMovingElement_thenElementIsmovedToNewPosition(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        expected_element = SlowMonster(A_POSITION + A_DELTA_POSITION, SOME_ENERGY)
        self.assertIn(expected_element, world_elements)

    def test_whenMovingElement_thenMagnitudeOfMovementIsRemovedFromEnergy(self):
        energy = create_autospec(Energy)
        world_elements = WorldElements({A_MONSTER})

        world_elements.move(A_MONSTER, A_DELTA_POSITION, energy)

        energy.remove.assert_called_once_with(A_DELTA_POSITION.magnitude())

    def test_givenNotEnoughEnergy_whenMovingElement_thenExceptionIsRaised(self):
        energy = create_autospec(Energy)
        energy.remove.side_effect = NoMoreEnergy
        world_elements = WorldElements({A_MONSTER})
        arguments = (A_MONSTER, A_DELTA_POSITION, energy)

        self.assertRaises(NotEnoughEnergyToMove, world_elements.move, *arguments)

    def test_givenNotEnoughEnergy_whenMovingElement_thenElementIsNotMoved(self):
        energy = create_autospec(Energy)
        energy.remove.side_effect = NoMoreEnergy
        world_elements = WorldElements({A_MONSTER})

        silence(world_elements.move)(A_MONSTER, A_DELTA_POSITION, energy)

        self.assertIn(A_MONSTER, world_elements)


def silence(function):
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            pass

    return decorator
