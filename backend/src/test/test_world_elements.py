import unittest
from unittest.mock import create_autospec

from src.position import Position
from src.monster.slow_monster import SlowMonster
from src.world_elements import WorldElements

A_POSITION = Position(1, 1)


class WorldElementsTest(unittest.TestCase):
    def test_whenRemovingElement_thenElementIsRemoved(self):
        element = SlowMonster(A_POSITION)
        world_elements = WorldElements({element})

        world_elements.remove(element)

        self.assertTrue(world_elements.is_empty())
        self.assertFalse(world_elements.has(element))

    def test_whenAddingElement_thenElementIsAdded(self):
        element = SlowMonster(A_POSITION)
        world_elements = WorldElements(set())

        world_elements.add(element)

        self.assertFalse(world_elements.is_empty())
        self.assertTrue(world_elements.has(element))
