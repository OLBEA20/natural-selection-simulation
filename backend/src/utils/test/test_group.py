import unittest

from src.utils.group import group

KEY_1 = "1"
KEY_2 = "2"


class GroupTest(unittest.TestCase):
    def test_givenElementWithSameKey_whenGroupingElements_thenElementsAreGrouped(self):
        element_1 = KEY_1
        element_2 = KEY_1
        elements = [element_1, element_2]

        grouped_elements = group(elements, key=lambda element: element)

        expected_grouped_elements = [(KEY_1, [KEY_1, KEY_1])]
        self.assertEqual(expected_grouped_elements, list(grouped_elements))

    def test_givenElementWithDifferentKey_whenGroupingElements_thenElementsAreNotGrouped(
        self
    ):
        element_1 = KEY_1
        element_2 = KEY_2
        elements = [element_1, element_2]

        grouped_elements = group(elements, key=lambda element: element)

        expected_grouped_elements = [(KEY_1, [KEY_1]), (KEY_2, [KEY_2])]
        self.assertEqual(expected_grouped_elements, list(grouped_elements))

    def test_givenNoElements_whenGroupingElements_thenNoGroups(self):
        grouped_elements = group([], key=lambda element: element)

        expected_grouped_elements = []
        self.assertEqual(expected_grouped_elements, list(grouped_elements))
