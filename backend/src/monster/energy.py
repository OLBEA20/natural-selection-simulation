from __future__ import annotations


class Energy:
    def __init__(self, value: float):
        self.value: float = value

    def remove(self, value_to_remove: float):
        self.value -= value_to_remove
        if self.value <= 0:
            raise NoMoreEnergy

    def add(self, energy: Energy):
        self.value += energy.value
        energy.value = 0


class NoMoreEnergy(Exception):
    pass
