import unittest

from src.monster.energy import Energy, NotEnoughEnergy
from src.utils.silence import silence

INITIAL_VALUE = 10
SOME_VALUE = INITIAL_VALUE - 2


class EnergyTest(unittest.TestCase):
    def test_whenRemovingEnergy_thenEnergyIsRemoved(self):
        energy = Energy(INITIAL_VALUE)

        energy.remove(SOME_VALUE)

        self.assertEqual(INITIAL_VALUE - SOME_VALUE, energy.value)

    def test_givenNotEnoughEnergy_whenRemovingEnergy_thenExceptionIsRaised(self):
        energy = Energy(INITIAL_VALUE)

        self.assertRaises(NotEnoughEnergy, energy.remove, INITIAL_VALUE)

    def test_givenNotEnoughEnergy_whenRemovingEnergy_thenNoEnergyIsRemoved(self):
        energy = Energy(INITIAL_VALUE)

        silence(energy.remove)(INITIAL_VALUE)

        self.assertEqual(INITIAL_VALUE, energy.value)

    def test_whenAddingEnergyToEnergy_thenEnergyIsTransferred(self):
        energy = Energy(INITIAL_VALUE)
        energy_to_add = Energy(SOME_VALUE)

        energy.add(energy_to_add)

        self.assertEqual(INITIAL_VALUE + SOME_VALUE, energy.value)
        self.assertEqual(0, energy_to_add.value)

    def test_whenSplittingEnergy_thenHalfEnergyIsRemoved(self):
        energy = Energy(INITIAL_VALUE)

        energy.split()

        self.assertEqual(INITIAL_VALUE / 2, energy.value)

    def test_whenSplittingEnergy_thenHalfEnergyIsReturned(self):
        energy = Energy(INITIAL_VALUE)

        new_energy = energy.split()

        self.assertEqual(INITIAL_VALUE / 2, new_energy.value)

    def test_givenEnergyIsGreater_whenCheckingForGreaterOrEqual_thenTrue(self):
        energy = Energy(INITIAL_VALUE)
        greater_energy = Energy(INITIAL_VALUE + 1)

        self.assertGreaterEqual(greater_energy, energy)

    def test_givenEnergyIsEqual_whenCheckingForGreaterOrEqual_thenTrue(self):
        energy = Energy(INITIAL_VALUE)
        equal_energy = Energy(INITIAL_VALUE)

        self.assertGreaterEqual(equal_energy, energy)
