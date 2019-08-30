import unittest

from src.monster.energy import Energy, NoMoreEnergy

INITIAL_VALUE = 10
SOME_VALUE = INITIAL_VALUE - 2


class EnergyTest(unittest.TestCase):
    def test_whenRemovingEnergy_thenEnergyIsRemoved(self):
        energy = Energy(INITIAL_VALUE)

        energy.remove(SOME_VALUE)

        self.assertEqual(INITIAL_VALUE - SOME_VALUE, energy.value)

    def test_givenEnergyDropsBelowZero_whenRemovingEnergy_thenExceptionIsRaised(self):
        energy = Energy(INITIAL_VALUE)

        self.assertRaises(NoMoreEnergy, energy.remove, INITIAL_VALUE)
